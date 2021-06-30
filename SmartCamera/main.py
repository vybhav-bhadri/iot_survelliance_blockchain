from flask import Blueprint,render_template,Response
from . import db
from .camera import VideoCamera
import cv2
from .mail import sendEmail
import time
import sys
from flask_login import login_required, current_user
import os 

main = Blueprint('main', __name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_MODELS = os.path.join(APP_ROOT, 'models')
APP_MODELS_FACE = os.path.join(APP_ROOT, 'models/facial_recognition_model.xml')

email_update_interval = 600 # sends an email only once in this time interval
video_camera = VideoCamera(flip=True) # creates a camera object, flip vertically
object_classifier = cv2.CascadeClassifier(APP_MODELS_FACE) # an opencv classifier

last_epoch = 0

def check_for_objects():
	global last_epoch
	while True:
		try:
			frame, found_obj = video_camera.get_object(object_classifier)
			if found_obj and (time.time() - last_epoch) > email_update_interval:
				last_epoch = time.time()
				print ("Sending email...")
				sendEmail(frame) #print in our home as a notification
				print ("done!")
		except:
			print ("Error sending email: ", sys.exc_info()[0])


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


