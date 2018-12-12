# USAGE
# python main.py --cascade <cascade>

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
from multiprocessing import Process
from multiprocessing import Queue
from flask import Flask, render_template, Response
import numpy as np
import argparse
import imutils
import time
import cv2
import sys

app = Flask(__name__)

def classify_frame(body_cascade, inputQueue, outputQueue):
	# keep looping
	while True:
		# check to see if there is a frame in our input queue
		if not inputQueue.empty():
			# grab the frame from the inputQueue. Process it and detect object.
			frame = inputQueue.get()
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			detection = body_cascade.detectMultiScale(gray, 1.3, 5)
			# write the detection to the output queue
			outputQueue.put(detection)


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-ip", "--address", required=True, help="enter your local/home IP address")
ap.add_argument("-c", "--cascade", required=True,
	help="path to haar cascade xml file")
args = vars(ap.parse_args())

# load our haard cascade file
print("[INFO] loading haar cascade...")
body_cascade = cv2.CascadeClassifier(args["cascade"])
print("[INFO] Haar cascade loaded.")

# initialize the input queue (frames), output queue (detections),
# and the list of actual detections returned by the child process
inputQueue = Queue(maxsize=1)
outputQueue = Queue(maxsize=1)

# construct a child process *indepedent* from our main process of
# execution
print("[INFO] starting process...")
p = Process(target=classify_frame, args=(body_cascade, inputQueue,
	outputQueue,))
p.daemon = True
p.start()
	
# loop over the frames from the video stream
def gen():
        detection = None
	# initialize the video stream
	print("[INFO] loading rtsp stream...")
	vs = cv2.VideoCapture("rtsp://admin:admin@192.168.0.108:554/cam/realmonitor?channel=1&subtype=1")
	print("[INFO] done loading rtsp stream.")
	if vs.isOpened() == False:
		sys.exit("No ip stream found.")
		time.sleep(2.0)
	while True:
		# grab the frame from the threaded video stream, resize it, and
		# grab its dimensions
		ret, frame = vs.read()
		#frame = imutils.resize(frame, width=400)

		# if the input queue is empty, give the current frame to classify
		if inputQueue.empty():
			inputQueue.put(frame)

		# if the input queue is not empty, grab the detections
		if not outputQueue.empty():
			detection = outputQueue.get()

		#egray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		if detection is not None:
			for (x,y,w,h) in detection:
				cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0),2)
		# create jpeg frame for our index.html
		ret, jpeg = cv2.imencode('.jpg', frame)
		htmlframe = jpeg.tobytes()
		yield (b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + htmlframe + b'\r\n\r\n')
	vs.stop()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.run(host=args["address"], debug=True)
