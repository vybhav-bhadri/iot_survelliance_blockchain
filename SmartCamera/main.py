from flask import Blueprint,render_template,Response
from . import db
from .camera import VideoCamera
import cv2
import time
import sys
from flask_login import login_required, current_user
import os
import json
import base64
import requests
import datetime 

main = Blueprint('main', __name__)

#api address

api = 'http://192.168.1.9:8585/pidata'

api_test = 'http://192.168.1.9:8080/test'

#image address
image_file = ''

#device_id
device_id = 'ipcamera_1'

#face_id
face_id = 1

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_MODELS = os.path.join(APP_ROOT, 'models')
APP_MODELS_FACE = os.path.join(APP_ROOT, 'models/facial_recognition_model.xml')

image_update_interval = 10 # sends an json data only once in this time interval
video_camera = VideoCamera(flip=True) # creates a camera object, flip vertically
object_classifier = cv2.CascadeClassifier(APP_MODELS_FACE) # an opencv classifier

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@main.route('/')
@login_required
def index():
    return render_template('index.html',name=current_user.name)

@main.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),mimetype='multipart/x-mixed-replace; boundary=frame')

last_epoch = 0

def check_for_objects():
	global last_epoch
	global face_id
	while True:
		try:
			frame, found_obj = video_camera.get_object(object_classifier)
			if found_obj and (time.time() - last_epoch) > image_update_interval:
				last_epoch = time.time()
				timestamp = datetime.datetime.now()
				# timestamp = timestamp.strftime("%c")
				print("sending image to api..")
				im_bytes = frame
				# print('hey')
				im_b64 = base64.b64encode(im_bytes).decode("utf8")
				#json object(face_id,)
				# print('hey-1')
				payload = json.dumps({"Face_Id":face_id,"ImageData": im_b64,"Timestamp":timestamp,"Device_Id":device_id},default=str)
				# print('hey-2')
				response = requests.post(api_test, data=payload, headers=headers)
				# print('hey-3')
				face_id = face_id + 1
				print('done!')
		except:
			print ("Error sending image: ", sys.exc_info())




