#  Library things (Flask and opencv)
from flask import Flask, render_template, Response
import cv2

# this is for the line following and controlling the raspberry
import RPi.GPIO as IO

IO.setwarnings(False)
IO.setmode (IO.BCM)


IO.setup(2,IO.OUT) #GPIO 4 -> Motor 1 Terminal A
IO.setup(3,IO.OUT) #GPIO 14 -> Motor 2 Terminal B

IO.setup(4,IO.OUT) #GPIO 17  -> Motor LEFT Terminal A
IO.setup(17,IO.OUT) #GPIO 17  -> Motor LEFT Terminal B


# Start flask
app = Flask(__name__)

# This starts opencv and the camera stuff

camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read() # reads the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') # Concatonates the frames together
                   
@app.route('/')
def index():
    return render_template('index.html')    

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_button')
def stop_button():
    IO.output(4,True) #1A+
    IO.output(14,True) #1B-

    IO.output(17,True) #2A+
    IO.output(18,True) #2B-
    return res



if __name__ == '__main__':
    app.run(debug=True)
         