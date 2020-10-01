from flask import Flask, render_template, Response
import cv2
import time
from concurrent.futures import ThreadPoolExecutor

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor = 0.6

# Video Class only for detach image from an video, I use video instead of camera for an easy Demo Setup
class VideoCamera(object):
    def __init__(self, video_name):
        # self.video = cv2.VideoCapture(0)
        self.video = cv2.VideoCapture(video_name)

    def __del__(self):
        self.video.release()

    def reload(self):
        self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def get_frame_and_face_detector(self):
        success, image = self.video.read()
        if not success:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, image = self.video.read()
        image = cv2.resize(image, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in face_rects:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    def get_frame(self):
        success, image = self.video.read()
        if not success:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

app = Flask(__name__)
my_video1 = VideoCamera('video1.mp4')
frame1 = my_video1.get_frame()
my_video2 = VideoCamera('video2.mp4')
frame2 = my_video2.get_frame()
play = True
face_detector=True
speed = .300


@app.route('/')
def index():
    return render_template('index.html')

# Using python generator for update image (main core of streaming and broadcast)
def gen(video_id):
    while True:
        time.sleep(speed)
        if video_id == 1:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n\r\n')


# Main_ROle for select video  to load list image by image
@app.route('/video_feed/<int:video_id>')
def video_feed(video_id):
    return Response(gen(video_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# For Play Pause Button
@app.route('/play_pause', methods=['POST'])
def play_pause():
    global play
    play = not play
    return {"ok": "done"}


# For Speed Up Button
@app.route('/speed_up', methods=['POST'])
def speed_up():
    global speed
    speed = speed / 2
    return {"ok": "done"}


# For Speed Down Button
@app.route('/speed_down', methods=['POST'])
def speed_down():
    global speed
    speed = speed * 2
    return {"ok": "done"}

# For Reload Button
@app.route('/reload', methods=['POST'])
def reload():
    my_video1.reload()
    my_video2.reload()
    return {"ok": "done"}

@app.route('/on_of_face', methods=['POST'])
def on_of_face():
    global face_detector
    face_detector = not face_detector
    return {"ok": "done"}

# I create an easy demo of upload image for broadcast using load next image in video
def update_camera_image():
    global frame1
    global frame2
    while True:
        while play:
            time.sleep(speed)
            if face_detector:
                frame1 = my_video1.get_frame_and_face_detector()
                frame2 = my_video2.get_frame_and_face_detector()
            else:
                frame1 = my_video1.get_frame()
                frame2 = my_video2.get_frame()


executor = ThreadPoolExecutor(1)
if __name__ == '__main__':
    executor.submit(update_camera_image)
    app.run(host="0.0.0.0", port=4009, debug=False)
