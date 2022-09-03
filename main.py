# venv\Scripts\activate
# py main.py

import os
import shutil
from datetime import datetime

import numpy as np
import requests
from flask import Flask, jsonify, request

from utils import UTILS

app = Flask(__name__)

HTML_FORM = """
        <h1>Upload new File</h1>
        <form method="post" enctype="multipart/form-data">
        
            <label>image_file</label><br>
            <input type="file" name="image_file"><br><hr>

            <label>key</label><br>
            <input type="text" name="key"><br><hr>
            
            <label>user</label><br>
            <input type="text" name="user">
            
        <input type="submit">
        </form>
    """

    

@app.route("/api/blood51", methods=["GET", "POST"])
def generate_images():
    
    ut = UTILS()
    start = datetime.now()

    UPLOAD_FOLDER = "images\input_images"
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

    if request.method == "POST":
        if "image_file" not in request.files:
            return "There is no image_file in form!"

        image_file = request.files['image_file']
        user_name = str(request.form['user']).strip()
        key = str(request.form['key']).strip()

        image_path = os.path.join(UPLOAD_FOLDER, user_name + ".jpg")
        # image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
        image_file.save(image_path)
        
        result = ut.generate_images(image_path, user_name)
        
        if result:
            resp_list = {}
            user_output_folder = "images\output_images\{0}".format(user_name)
            list = os.listdir(user_output_folder)
            number_files = len(list)

            if number_files == 9:
                
                g_value_1 = ut.cropping("images/output_images/{0}/1.jpg".format(user_name))
                g_value_2 = ut.cropping("images/output_images/{0}/2.jpg".format(user_name))
                g_value_3 = ut.cropping("images/output_images/{0}/3.jpg".format(user_name))
                conc123 = ut.get_conc(g_value_1, g_value_2, g_value_3)

                g_value_4 = ut.cropping("images/output_images/{0}/4.jpg".format(user_name))
                g_value_5 = ut.cropping("images/output_images/{0}/5.jpg".format(user_name))
                g_value_6 = ut.cropping("images/output_images/{0}/6.jpg".format(user_name))
                conc456 = ut.get_conc(g_value_4, g_value_5, g_value_6)

                g_value_7 = ut.cropping("images/output_images/{0}/7.jpg".format(user_name))
                g_value_8 = ut.cropping("images/output_images/{0}/8.jpg".format(user_name))
                g_value_9 = ut.cropping("images/output_images/{0}/9.jpg".format(user_name))
                conc789 = ut.get_conc(g_value_7, g_value_8, g_value_9)

                print("g_value_1", g_value_1)
                print("g_value_2", g_value_2)
                print("g_value_3", g_value_3)
                print("g_value_4", g_value_4)
                print("g_value_5", g_value_5)
                print("g_value_6", g_value_6)
                print("g_value_7", g_value_7)
                print("g_value_8", g_value_8)
                print("g_value_9", g_value_9)

                resp_list.update({"1": str(conc123), "2": str(conc456), "3": str(conc789)})
                
            else:
                resp_list = {"1": "-1", "2": "-1", "3": "-1", "message": f"Number of images are {number_files}"}

        else:
            resp_list = {"1": str(result), "2": str(result), "3": str(result), "message": "Something is wrong with the image."}

        later = datetime.now()
        time_taken = (later - start).total_seconds()
        print("\ntime_taken", time_taken)
        print("\n", resp_list)

        return jsonify(resp_list)

    return HTML_FORM


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
