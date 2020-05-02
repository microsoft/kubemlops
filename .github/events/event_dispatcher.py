import argparse
from dispatch_event_handler import BaseDispatchEventHandler
from reg_model_event_handler import RegModelEventHandler
from start_train_event_handler import StartEventHandler
from finish_train_event_handler import FinishEventHandler


REGISTER_MODEL_EVENT = "Model is registered"
START_TRAIN_EVENT = "Training Started"
FINISH_TRAIN_EVENT = "Training Finished"


def get_event_handler(event_type):
    if (event_type == REGISTER_MODEL_EVENT):
        return RegModelEventHandler()
    elif (event_type == START_TRAIN_EVENT):
        return StartEventHandler()
    elif (event_type == FINISH_TRAIN_EVENT):
        return FinishEventHandler()
    else:
        return BaseDispatchEventHandler()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--event_type',
                        help='Event Type')
    args = parser.parse_args()

    event_dispatcher = get_event_handler(args.event_type)
    event_dispatcher.dispatch()
