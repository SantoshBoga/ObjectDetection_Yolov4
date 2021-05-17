import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app, flags, logging
from absl.flags import FLAGS
import core.utils as utils
from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
from PIL import Image
import os
import sys
import cv2
import time
import numpy as np
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
#from helping_functions import get_centroids, get_human_box_detection, get_points_from_box
from flask import Flask, request, Response, jsonify, send_from_directory, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS
import time as time
import boto3
from botocore.exceptions import NoCredentialsError

flags.DEFINE_string('framework', 'tf', '(tf, tflite, trt')
flags.DEFINE_string('weights', './checkpoints/custom-416',
                    'path to weights file')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny')
flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')
flags.DEFINE_string('image', './data/kite.jpg', 'path to input image')
flags.DEFINE_string('output', './base_react_app/src/detections/', 'path to output image')
flags.DEFINE_float('iou', 0.45, 'iou threshold')
flags.DEFINE_float('score', 0.25, 'score threshold')
FLAGS(sys.argv)

# Initialize Flask application
flask_app = Flask(__name__)
cors = CORS(flask_app, resources ={r"/detection": {"origins": "*"}})


config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)
STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(FLAGS)
saved_model_loaded = tf.saved_model.load(FLAGS.weights, tags=[tag_constants.SERVING])
infer = saved_model_loaded.signatures['serving_default']
input_size = FLAGS.size


ACCESS_KEY = ''
SECRET_KEY = ''


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file,ExtraArgs={'ACL': 'public-read'})
        print("Upload Successful")
        url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
                'Bucket': bucket,
                'Key': s3_file
                
            }
        )
        print(url)
        return url
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False




# API that returns JSON with classes found in images
@flask_app.route('/detection', methods=['POST'])
def human_detect():
    image = request.files["file"]
    image_path = image.filename
    image.save(os.path.join(os.getcwd(), image_path))
    if image_path != "":
        original_image = cv2.imread(f"./{image_path}")
        # print(original_image.shape)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        # print('Boga')

        image_data = cv2.resize(original_image, (input_size, input_size))
        image_data = image_data / 255.
        images_data = []
        for i in range(1):
            images_data.append(image_data)
        #image_data = image_data[np.newaxis, ...].astype(np.float32)
        images_data = np.asarray(images_data).astype(np.float32)
        # print(images_data.shape)
        batch_data = tf.constant(images_data)
        # print('Sai')
        # print(batch_data.shape)
        #print(saved_model_loaded)
        infer = saved_model_loaded.signatures['serving_default']
        pred_bbox = infer(batch_data)
        # print('Santosh')
        # print(pred_bbox)

        for key, value in pred_bbox.items():
            boxes = value[:, :, 0:4]
            pred_conf = value[:, :, 4:]

        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=FLAGS.iou,
            score_threshold=FLAGS.score
        )
        #final_boxes = boxes.numpy()
        #final_scores = scores.numpy()
        #final_classes = classes.numpy()
        pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
        image = utils.draw_bbox(original_image, pred_bbox)
        image = Image.fromarray(image.astype(np.uint8))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        cv2.imwrite(FLAGS.output  + str(image_path[:-4]) + '_detection' +'.jpg', image)
        file_name = str(image_path[:-4])+ '_detection'+'.jpg'
        print(FLAGS.output+file_name)
        uploaded = upload_to_aws(FLAGS.output+file_name, 'yolov4-images', file_name)
        #print(uploaded)

        #array_boxes_detected = []
        #if len(boxes)>0:
        #    array_boxes_detected = get_human_box_detection(final_boxes,final_scores[0].tolist(),final_classes[0].tolist(),original_image.shape[0],original_image.shape[1])
        time.sleep(2)
        try:
            print(uploaded.split("?")[0])
            return str(uploaded.split("?")[0]), 200
        except FileNotFoundError:
            abort(404)

if __name__ == '__main__':
    flask_app.run(debug=True, host = '127.0.0.1', port=5000)