from flask import Flask, render_template,url_for, request,redirect,send_file
from werkzeug.utils import secure_filename
import os
from os import path
import cv2



app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")



@app.route("/convert", methods=["GET", "POST"] )
def convert():

    if request.method == "POST":

        if request.files:
            video = request.files["video"]
            video.save(secure_filename(video.filename))
            print(video.filename)

            cap= cv2.VideoCapture(video.filename)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            fps=cap.get(cv2.CAP_PROP_FPS)
            ret, img=cap.read()
            height,width,layers=img.shape
            size=(width,height)
            out_name="video_output.mp4"
            video.save('video_output.mp4')
            out= cv2.VideoWriter('video_output.mp4',fourcc,fps,size,0)
            while(cap.isOpened()):
                ret, frame = cap.read();
                if ret == True:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    out.write(gray)
                else:
                    break
            cap.release()
            out.release()
            os.remove(video.filename)
            return send_file(out_name,as_attachment=True)

    return render_template("convert.html")










@app.route("/about")
def about():
	return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
