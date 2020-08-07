# Logging
# TODO:
# - Config file
# - Refactor to plug in to serving
# - Should we wrap an already customized unhandled exp handler?
# - Structured TF/non-TF azure log levels
# - Use OpenCensus logger integration?
# - Mock tests
# - Doc'ified comments
# - Duplicate stderr fix
# - Trace/span uuid for run, ordering
# - Remove noise from Azure Monitor
# - Remove noise from OpenCensus on command line
# - Add run start/end time to init/cooldown

import sys
import os
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.trace import config_integration, span
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
from opencensus.trace.logging_exporter import LoggingExporter
import inspect
import json

# Add traceId and spanId context information to the available logging
# format specifiers.
config_integration.trace_integrations(['logging'])

# Simple filter to restrict the upper bound of a log level. For example, it is
# desireable to stop stdout from printing WARNING and ERROR. Combined with the
# built in log level in the handler, this effectively gives us a range.
class MaxLevelFilter(object):
    def __init__(self, level):
        self.level = level

    def filter(self, logRecord):
        return logRecord.levelno <= self.level


def init_console_logging(logger):
    # console_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(filename)s:%(lineno)s - %(message)s')   # noqa: E501

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_formatter = logging.Formatter('stderr_handler: %(levelname)s: traceId=%(traceId)s spanId=%(spanId)s %(filename)s:%(lineno)s - %(message)s')   # noqa: E501
    stderr_handler.setFormatter(stderr_formatter)
    logger.addHandler(stderr_handler)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(MaxLevelFilter(logging.WARNING))
    stdout_formatter = logging.Formatter('stdout_handler: %(levelname)s: traceId=%(traceId)s spanId=%(spanId)s %(filename)s:%(lineno)s - %(message)s')   # noqa: E501
    stdout_handler.setFormatter(stdout_formatter)
    logger.addHandler(stdout_handler)

def init_azure_logging(logger):
    azure_monitor_key = os.environ.get('APPLICATIONINSIGHTS_CONNECTION_STRING')
    if not azure_monitor_key:
        print('AppInsights logging disabled')
        return

    azure_log_handler = AzureLogHandler()  # Implicit key from env
    azure_log_handler.setLevel(logging.DEBUG)
    logger.addHandler(azure_log_handler)
    print('AppInsights logging initialized')


def init_opencensus_tracer(logger):
    tracer = Tracer(
        exporter=LoggingExporter(),  # Implicit key from env
        sampler=ProbabilitySampler(1.0)  # Always log, reduce to sample
    )
    print('Tracer initialized')
    return tracer


class MLFlowContextFilter(logging.Filter):
    # TODO(tcare): reduce overhead by lazily updating or caching this.
    def get_mlflow_run_data(self):
        # If MLFlow hasn't been loaded by the caller, we're done.
        if not sys.modules.get('mlflow'):
            print('No MLFlow run data')
            return {}

        import mlflow
        client = mlflow.tracking.MlflowClient()
        active_run = mlflow.active_run()
        if not active_run:
            print('No MLFlow run data')
            return None
        run_id = active_run.info.run_id
        data = client.get_run(run_id).data
        print('Added MLFlow run data:')
        print(data.to_dictionary())
        return data.to_dictionary()

    def filter(self, record):
        run_data = self.get_mlflow_run_data()
        if run_data:
            # The field needs to be named this way for AppInsights to use it.
            record.custom_dimensions = {
                'metrics': json.dumps(run_data['metrics']),
                'tags': json.dumps(run_data['tags']),
                'params': json.dumps(run_data['params']),
            }

        # Allow the record to propagate
        return True

def get_tracer():
    return tracer

def get_logger():
    return logger

print('Initializing logging...')
logger = logging.getLogger(__name__)  # Get root logger.
mlflow_filter = MLFlowContextFilter()

logger.addFilter(mlflow_filter)
#logger.propagate = False

# Log everything by default, delegate to handlers for their own levels.
logger.setLevel(logging.DEBUG)

# logger.debug('debug')
# logger.info('info')
#ogger.warning('warning')
#logger.error('error')
#logger.exception('exception')


init_console_logging(logger)
init_azure_logging(logger)
tracer = init_opencensus_tracer(logger)
print('Logging initialized')

# logger.debug('debug')
# logger.info('info')
# logger.warning('warning')
# logger.error('error')
# logger.exception('exception')

# with tracer.span('parent'):
#     with tracer.span('child'):
#         logger.debug('debug')
#         logger.info('info')
#         logger.warning('warning')
#         logger.error('error')
