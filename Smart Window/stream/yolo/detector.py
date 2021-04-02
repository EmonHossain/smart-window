import colorsys
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import cv2
import time

import numpy as np
from keras import backend as K
from keras.models import load_model
from keras.layers import Input

from yolo3.model import yolo_eval, yolo_body, tiny_yolo_body
from yolo3.utils import image_preporcess


class YOLO(object):

    _defaults = {
        "model_path": 'model_data/yolo_custom_weights.h5',
        "anchors_path": 'model_data/yolo_anchors.txt',
        "classes_path": 'model_data/yolo_classes.txt',
        "score": 0.3,
        "iou": 0.45,
        "model_image_size": (320, 320),
        "text_size": 1,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)  # set up default values
        self.__dict__.update(kwargs)  # and update with user overrides
        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        self.sess = K.get_session()
        self.boxes, self.scores, self.classes = self.generate()

    def _get_class(self):
        classes_path = os.path.expanduser(self.classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def _get_anchors(self):
        anchors_path = os.path.expanduser(self.anchors_path)
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape(-1, 2)

    def generate(self):
        model_path = os.path.expanduser(self.model_path)
        assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

        # Load model, or construct model and load weights.
        num_anchors = len(self.anchors)
        num_classes = len(self.class_names)
        is_tiny_version = num_anchors == 6  # default setting
        try:
            self.yolo_model = load_model(model_path, compile=False)
        except:
            self.yolo_model = tiny_yolo_body(Input(shape=(None, None, 3)), num_anchors // 2, num_classes) \
                if is_tiny_version else yolo_body(Input(shape=(None, None, 3)), num_anchors // 3, num_classes)
            self.yolo_model.load_weights(self.model_path)  # make sure model, anchors and classes match
        else:
            assert self.yolo_model.layers[-1].output_shape[-1] == \
                   num_anchors / len(self.yolo_model.output) * (num_classes + 5), \
                'Mismatch between model and given anchor and class sizes'

        print('{} model, anchors, and classes loaded.'.format(model_path))

        # Generate colors for drawing bounding boxes.
        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))

        np.random.shuffle(self.colors)  # Shuffle colors to decorrelate adjacent classes.

        # Generate output tensor targets for filtered bounding boxes.
        self.input_image_shape = K.placeholder(shape=(2,))
        boxes, scores, classes = yolo_eval(self.yolo_model.output, self.anchors,
                                           len(self.class_names), self.input_image_shape,
                                           score_threshold=self.score, iou_threshold=self.iou)
        return boxes, scores, classes

    def detect_image(self, image):
        if self.model_image_size != (None, None):
            assert self.model_image_size[0] % 32 == 0, 'Multiples of 32 required'
            assert self.model_image_size[1] % 32 == 0, 'Multiples of 32 required'
            boxed_image = image_preporcess(np.copy(image), tuple(reversed(self.model_image_size)))
            image_data = boxed_image

        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [image.shape[0], image.shape[1]],  # [image.size[1], image.size[0]],
                #K.learning_phase(): 0
            })

        ObjectsList = []

        for i, c in reversed(list(enumerate(out_classes))):
            predicted_class = self.class_names[c]
            print("found : "+predicted_class)
            ObjectsList.append(predicted_class)

        return ObjectsList

    def close_session(self):
        self.sess.close()

    def detect_img(self, image):
        #imag = cv2.imread(image, cv2.IMREAD_COLOR)
        imag = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        original_image = cv2.cvtColor(imag, cv2.COLOR_BGR2RGB)
        original_image_color = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        _poi_desc = {
            "karl_marx": "The Karl Marx Monument is a 7.10m-tall stylized head of Karl Marx in Chemnitz, Germany.",
            "opera_house": "The Chemnitz Opera House is the main venue for the music theater sections of the Chemnitz Theater. It was built in Chemnitz from 1906 to 1909",
        }
        _poi_title = {
            "karl_marx": "Karl marx monument",
            "opera_house": "Opera House Chemnitz",
        }
        _poi_img = {
            "karl_marx": "/static/stream/images/cm.png",
            "opera_house": "/static/stream/images/opera.png"
        }

        ObjectsList = self.detect_image(original_image_color)
        _json_data = {
            'found': 0,
            'poi': "",
            'desc': "",
            'img': ""
        }
        if len(ObjectsList) != 0:
            _json_data['found'] = 1
            _json_data['poi'] = _poi_title[str(ObjectsList[0])]
            _json_data['desc'] = _poi_desc[str(ObjectsList[0])]
            _json_data['img'] = _poi_img[str(ObjectsList[0])]
        return _json_data


