import time
from io import BytesIO
import datetime
import requests
import numpy as np
from PIL import Image
import tensorflow as tf
import kfserving
from typing import Dict


class KFServingSampleModel(kfserving.KFModel):

    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.ready = False

    def load(self):
        print('Attempting to load model')
        model = tf.keras.models.load_model('/app/model.h5')
        model.summary()
        self.model = model
        self.ready = True
        print('Done!')

    def process_image(self, path, image_size):
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

    def predict(self, request: Dict) -> Dict:
        prev_time = time.time()
        img_path = request['image']
        current_time = time.time()

        tensor = self.process_image(img_path, 160)
        t = tf.reshape(tensor, [-1, 160, 160, 3])
        o = self.model.predict(t, steps=1)  # [0][0]
        print(o)
        o = o[0][0]
        inference_time = datetime.timedelta(seconds=current_time - prev_time)
        payload = {
            'time': inference_time.total_seconds(),
            'prediction': 'burrito' if o > 0.5 else 'tacos',
            'scores': str(o)
        }

        print('Input ({}), Prediction ({})'.format(img_path, payload))

        return payload


if __name__ == "__main__":
    model = KFServingSampleModel("mexicanfood")
    model.load()
    kfserving.KFServer(workers=1).start([model])
