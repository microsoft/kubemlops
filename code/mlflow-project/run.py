import mlflow
import os
import click
import kubemlops.logging

logger = kubemlops.logging.get_logger()


@click.command()
@click.option("--experiement_id", type=click.INT)
@click.option("--kf_run_id", type=click.STRING)
def run(experiement_id, kf_run_id):
    mlflow.set_tracking_uri("databricks")
    submitted_run = mlflow.run(".",
                               entry_point="main",
                               experiment_name=None,
                               experiment_id=experiement_id,
                               parameters=None,
                               backend='databricks',
                               backend_config='clusterconfig.json',
                               )
    mlflowClient = mlflow.tracking.MlflowClient().get_run(submitted_run.run_id)
    if (mlflowClient.info.status != "FINISHED"):
        raise Exception("MLflow Experiment failed")

    logger.info("Experiment Completed")
    logger.info("Status: " + mlflowClient.info.status)
    logger.info("MLFLOW Run ID: " + mlflowClient.info.run_id)
    logger.info("MLFLOW Artifact URI" + mlflowClient.info.artifact_uri)
    logger.info("KubeFlow Run ID" + kf_run_id)


if __name__ == '__main__':
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    print(os.path.abspath(os.getcwd()))
    run()
