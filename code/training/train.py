from __future__ import absolute_import, division, print_function
import os
import sys
import math
import hmac
import json
import hashlib
import argparse
from random import shuffle, random
from pathlib2 import Path
import numpy as np
import tensorflow as tf
from tensorflow.data import Dataset
from tensorflow.python.lib.io import file_io
import pandas as pd
import mlflow
import mlflow.tensorflow

import ml_logging
import logging
import inspect

# Custom exception handler to override the system exception hook.
# Note this is for last resort, unhandled exceptions only. It should not be
# used as a general exception handler.
# https://docs.python.org/3/library/sys.html#sys.excepthook

exception_handler_save = sys.excepthook


def exception_handler(type, value, traceback):
    # Restore the original handler in case our code triggers more exceptions.
    # It may not be our fault, e.g. not enough stack space, OOM.
    sys.excepthook = exception_handler_save

    # Allow some special exception types through.
    if issubclass(type, KeyboardInterrupt):
        return

    logger = logging.getLogger(__name__)

    logger.exception(msg='Unhandled exception', exc_info=(type, value, traceback))  # noqa: E501

    # Pass through to original handler
    return sys.excepthook(type, value, traceback)


def install_exception_handler():
    # Python provides the original exception handler as sys.__excepthook__,
    # However it's possible that something else already overwrote it.
    if sys.excepthook != sys.__excepthook__:
        # Sanity check to see if it is our hook.
        if sys.excepthook == exception_handler:
            raise Exception('Duplicate exception handler - did you already install it?')  # noqa: E501
        # TODO(tcare): Looks like this can be false if the OS (e.g. Ubuntu)
        # overrides the handler. Can we tell if it's a system handler
        # that doesn't originate from python?
        else:
            logger.warning('External exception handler installed - ' + str(inspect.getsourcefile(sys.excepthook)))  # noqa: E501
        #    raise Exception('Other exception handler already installed')

    # Overwrite the hook
    sys.excepthook = exception_handler

    print('Exception hook installed')


logger = ml_logging.get_logger()
install_exception_handler()
tracer = ml_logging.get_tracer()


def check_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return Path(path).resolve(strict=False)


def process_image(path, label, img_size):
    img_raw = tf.io.read_file(path)
    img_tensor = tf.image.decode_jpeg(img_raw, channels=3)
    img_final = tf.image.resize(img_tensor, [img_size, img_size]) / 255
    return img_final, label


def load_dataset(base_path, dset, split=None):
    # normalize splits
    if split is None:
        split = [8, 1, 1]
    splits = np.array(split) / np.sum(np.array(split))

    # find labels - parent folder names
    labels = {}
    for (_, dirs, _) in os.walk(base_path):
        logger.info('found {}'.format(dirs))
        labels = {k: v for (v, k) in enumerate(dirs)}
        logger.info('using {}'.format(labels))
        break

    # load all files along with idx label
    logger.info('loading dataset from {}'.format(dset))
    with open(dset, 'r') as d:
        data = [(str(Path(line.strip()).absolute()),
                 labels[Path(line.strip()).parent.name]) for line in d.readlines()]  # noqa: E501

    logger.info('dataset size: {}\nsuffling data...'.format(len(data)))

    # shuffle data
    shuffle(data)

    logger.info('splitting data...')
    # split data
    train_idx = int(len(data) * splits[0])

    return data[:train_idx]


# @print_info
def run(
        dpath,
        img_size=160,
        epochs=10,
        batch_size=32,
        learning_rate=0.0001,
        output='model',
        dset=None,
        metrics_file='/mlpipeline-metrics.json'):

    global g_image_size
    g_image_size = img_size
    img_shape = (img_size, img_size, 3)

    logger.info('Loading Data Set')
    # load dataset
    with tracer.span(name='Dataset Init'):
        train = load_dataset(dpath, dset)

        # training data
        train_data, train_labels = zip(*train)
        train_ds = Dataset.zip((Dataset.from_tensor_slices(list(train_data)),
                                Dataset.from_tensor_slices(list(train_labels)),
                                Dataset.from_tensor_slices([img_size]*len(train_data))))  # noqa: E501

        logger.info(train_ds)
        train_ds = train_ds.map(map_func=process_image,
                                num_parallel_calls=5)

        train_ds = train_ds.apply(tf.data.experimental.ignore_errors())

        train_ds = train_ds.batch(batch_size)
        train_ds = train_ds.prefetch(buffer_size=5)
        train_ds = train_ds.repeat()

    # model
    logger.info('Creating Model')
    with tracer.span(name='Model Creation'):
        base_model = tf.keras.applications.MobileNetV2(input_shape=img_shape,
                                                       include_top=False,
                                                       weights='imagenet')
        base_model.trainable = True

        model = tf.keras.Sequential([
            base_model,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        model.compile(optimizer=tf.keras.optimizers.Adam(lr=learning_rate),
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

        model.summary()

    # training
    logger.info('Training')
    with tracer.span(name='Model Training'):
        steps_per_epoch = math.ceil(len(train) / batch_size)
        mlflow.tensorflow.autolog()
        model.fit(train_ds, epochs=epochs, steps_per_epoch=steps_per_epoch)

    with tracer.span(name='Post Training'):
        # Log metric
        # TODO calculate metric from based on evalution data.
        # accuracy = model.evaluate()
        accuracy = random()  # dummy score
        metric = {
            'name': 'accuracy-score',
            'numberValue':  accuracy,
            'format': "PERCENTAGE",
        }
        metrics = {                          # [doc] https://www.kubeflow.org/docs/pipelines/sdk/pipelines-metrics/  # noqa: E501
            'metrics': [metric]}

        # TODO
        # It would be nice to refactor all this infra code below like logging, saving files,  # noqa: E501
        # out of this method so it just does the training and returns the model along with metrics  # noqa: E501

        # Log to mlflow
        mlflow.log_metrics({"accuracy": accuracy})

        # Pipeline Metric
        logger.info('Writing Pipeline Metric')
        with file_io.FileIO(metrics_file, 'w') as f:
            json.dump(metrics, f)

    # save model
    logger.info('Saving Model')
    with tracer.span(name='Model Saving'):

        # check existence of base model folder
        output = check_dir(output)

        logger.info('Serializing into saved_model format')
        tf.saved_model.save(model, str(output))
        logger.info('Done!')

        # add time prefix folder
        file_output = str(Path(output).joinpath('latest.h5'))
        logger.info('Serializing h5 model to:\n{}'.format(file_output))
        model.save(file_output)
        # mlflow.log_artifact(file_output)

        return generate_hash(file_output, 'kf_pipeline')


def generate_hash(dfile, key):
    logger.info('Generating hash for {}'.format(dfile))
    m = hmac.new(str.encode(key), digestmod=hashlib.sha256)
    BUF_SIZE = 65536
    with open(str(dfile), 'rb') as myfile:
        while True:
            data = myfile.read(BUF_SIZE)
            if not data:
                break
            m.update(data)

    return m.hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='transfer learning for binary image task')
    parser.add_argument('-s', '--base_path',
                        help='directory to base data', default='../../data')
    parser.add_argument(
        '-d', '--data', help='directory to training and test data', default='train')  # noqa: E501
    parser.add_argument(
        '-e', '--epochs', help='number of epochs', default=10, type=int)
    parser.add_argument('-b', '--batch', help='batch size',
                        default=32, type=int)
    parser.add_argument('-i', '--image_size',
                        help='image size', default=160, type=int)
    parser.add_argument('-l', '--lr', help='learning rate',
                        default=0.0001, type=float)
    parser.add_argument('-o', '--outputs',
                        help='output directory', default='model')
    parser.add_argument('-f', '--dataset', help='input dataset', required=True)
    parser.add_argument(
        '-m', '--model', help='output model info', required=True)
    parser.add_argument('-u', '--ui_metadata',
                        help='ui metadata', required=True)
    parser.add_argument('-me', '--metrics',
                        help='model metrics', required=True)
    args = parser.parse_args()

    logger.info('Using TensorFlow v.{}'.format(tf.__version__))

    data_path = Path(args.base_path).joinpath(args.data).resolve(strict=False)
    target_path = Path(args.base_path).resolve(
        strict=False).joinpath(args.outputs)
    dataset = Path(args.base_path).joinpath(args.dataset)
    image_size = args.image_size

    output_model_file = Path(args.model).resolve(strict=False)
    Path(output_model_file).parent.mkdir(parents=True, exist_ok=True)

    ui_metadata_file = Path(args.ui_metadata).resolve(strict=False)
    Path(ui_metadata_file).parent.mkdir(parents=True, exist_ok=True)

    metrics_file = Path(args.metrics).resolve(strict=False)
    Path(metrics_file).parent.mkdir(parents=True, exist_ok=True)

    params = Path(args.base_path).joinpath('params.json')

    args = {
        "dpath": str(data_path),
        "img_size": image_size,
        "epochs": args.epochs,
        "batch_size": args.batch,
        "learning_rate": args.lr,
        "output": str(target_path),
        "dset": str(dataset),
        "metrics_file": str(metrics_file)
    }

    dataset_signature = generate_hash(dataset, 'kf_pipeline')
    # printing out args for posterity
    for i in args:
        logger.info('{} => {}'.format(i, args[i]))

    # Log to mlflow
    mlflow.set_experiment("mexicanfood")
    mlflow.set_tag("external_run_id", os.environ.get("RUN_ID"))

    model_signature = run(**args)

    args['dataset_signature'] = dataset_signature.upper()
    args['model_signature'] = model_signature.upper()
    args['model_type'] = 'tfv2-MobileNetV2'
    #  mlflow.log_params(args)
    logger.info('Writing out params...')
    with open(str(params), 'w') as f:
        json.dump(args, f)

    logger.info('Saved to {}'.format(str(params)))

    logger.info('Log Traning Parameters')
    parmeters = pd.read_json(str(params), typ='series')
    metadata = {
        'outputs': [{
            'type': 'table',
            'storage': 'inline',
            'format': 'csv',
            'header': ['Name', 'Value'],
            'source': parmeters.to_csv()
        }]
    }

    # Path(output_path).parent.`mkdir(parents=True, exist_ok=True)
    with open(str(ui_metadata_file), 'w') as f:
        json.dump(metadata, f)

    model_output_content = []
    for filename in target_path.iterdir():
        model_output_content.append(str(filename))

    with open(str(output_model_file), 'w+') as f:
        f.write('\n'.join(model_output_content))
