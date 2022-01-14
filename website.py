#  Library things (Flask and opencv)
from flask import Flask, render_template, Response
import cv2

# This library is used for the ultrasonic sensor
import time

# this library is used for developing for the raspberry pi on windows or macos
import importlib.util

# This code check if the RPi.GPIO library is installed if not it fakes it.
try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as IO
except ImportError:
    """
    import FakeRPi.GPIO as GPIO
    OR
    import FakeRPi.RPiO as RPiO
    """
	
    import FakeRPi.GPIO as IO


# declaring the pins for the ultrasonic sensor
GPIO_TRIGGER = 18
GPIO_ECHO = 24

# this is for the line following and controlling the raspberry


IO.setwarnings(False)
IO.setmode (IO.BCM)


IO.setup(2,IO.OUT) #GPIO 4 -> Motor 1 Terminal A
IO.setup(3,IO.OUT) #GPIO 14 -> Motor 2 Terminal B

IO.setup(4,IO.OUT) #GPIO 17  -> Motor LEFT Terminal A
IO.setup(17,IO.OUT) #GPIO 17  -> Motor LEFT Terminal B


# Setuping up thg gpio for the ultrasonic sensors
IO.setup(GPIO_TRIGGER,IO.OUT)
IO.setup(GPIO_ECHO,IO.IN)

# this starts he measuring.
def distance():
    IO.output(GPIO_TRIGGER, True)

    time.sleep(0.00001)
    IO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # This saves the start time
    while IO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # Saves time of arrival back to the sensor
    while IO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # this finds the difference between the two times to find the distance
    TimeElapsed = StopTime - StartTime
    # multiple by Sonic speed (34300 cm/s) then divide by 2 as it has to go thee and back.
    distance = (TimeElapsed * 34300) / 2

    return distance



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

# this makes the robot stop button work
@app.route('/stop_button')
def stop_button():
    IO.output(4,True) #1A+
    IO.output(14,True) #1B-

    IO.output(17,True) #2A+
    IO.output(18,True) #2B-
    return res


# This makes the line following button work.
@app.route('/line_button')
def line_button():
    if(IO.input(2)==True and IO.input(3)==True):  #checks if both ir sensors are on white
        IO.output(4,True) #1A+
        IO.output(14,False) #1B-

        IO.output(17,True) #2A+
        IO.output(18,False) #2B-

    elif(IO.input(2)==False and IO.input(3)==True): #turn right
        IO.output(4,True) #1A+
        IO.output(14,True) #1B-

        IO.output(17,True) #2A+
        IO.output(18,False) #2B-

    elif(IO.input(2)==True and IO.input(3)==False): #Turn left
        IO.output(4,True) #1A+
        IO.output(14,False) #1B-

        IO.output(17,True) #2A+
        IO.output(18,True) #2b-

    else: #This makes the robot stay still
        IO.output(4,True) #1A+
        IO.output(14,True) #1B-

        IO.output(17,True) #2A+
        IO.output(18,True) #2B-

    dist = distance()

    # this stops the robot if within 10cm of an object in front of the ultrasonic sensor.
    if dist <= 10:
        IO.output(4,True)
        IO.output(14,True)

        IO.output(17,True)
        IO.output(18,True)
    return res



if __name__ == '__main__':
    app.run(debug=True)
         