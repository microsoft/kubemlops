import json
from io import BytesIO
import datetime
import requests
import numpy as np
from PIL import Image
import tensorflow as tf
from azureml.core.model import Model
import pandas as pd


def init():
    global model
    if Model.get_model_path('tacosandburritos'):
        model_path = Model.get_model_path('tacosandburritos')
    else:
        model_path = '/model/latest.h5'

    print('Attempting to load model')
    model = tf.keras.models.load_model(model_path)
    model.summary()
    print('Done!')

    print('Initialized model "{}" at {}'.format(
        model_path, datetime.datetime.now()))


def run(raw_data):

    post = json.loads(raw_data)
    img_path = post['image']

    tensor = process_image(img_path, 160)
    t = tf.reshape(tensor, [-1, 160, 160, 3])
    vol_shape = t.numpy().shape[:-1]
    n_voxels = np.prod(vol_shape)
    voxel_2d = t.numpy().reshape(n_voxels, t.numpy().shape[-1])
    header = {"content-type": "application/json; format=pandas-split"}
    df = pd.DataFrame(data=voxel_2d)
    json_str = df.to_json(orient='split')
    o = requests.post("http://localhost:8080/invocations", json=json_str, headers=header)  # noqa: E501
    print(o.content)


def process_image(path, image_size):
    # Extract image (from web or path)
    if path.startswith('http'):
        response = requests.get(path)
        img = np.array(Image.open(BytesIO(response.content)))
    else:
        img = np.array(Image.open(path))

    img_tensor = tf.convert_to_tensor(img, dtype=tf.float32)
    # tf.image.decode_jpeg(img_raw, channels=3)
    img_final = tf.image.resize(img_tensor, [image_size, image_size]) / 255
    return img_final


def info(msg, char="#", width=75):
    print("")
    print(char * width)
    print(char + "   %0*s" % ((-1 * width) + 5, msg) + char)
    print(char * width)


if __name__ == "__main__":
    images = {
        'tacos': 'https://c1.staticflickr.com/5/4022/4401140214_f489c708f0_b.jpg',  # noqa: E501
        'burrito': 'https://www.exploreveg.org/files/2015/05/sofritas-burrito.jpeg'  # noqa: E501
    }

    # init()

    for k, v in images.items():
        print('{} => {}'.format(k, v))

    info('Taco Test')
    taco = json.dumps({'image': images['tacos']})
    print(taco)
    run(taco)

    info('Burrito Test')
    burrito = json.dumps({'image': images['burrito']})
    print(burrito)
    run(burrito)
