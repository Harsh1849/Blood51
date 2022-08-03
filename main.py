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

    

@app.route("/api/generate_images", methods=["GET", "POST"])
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
        user_name = request.form['user']
        key = request.form['key']

        image_path = os.path.join(UPLOAD_FOLDER, user_name + ".jpg")
        # image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
        image_file.save(image_path)
        
        result = ut.generate_images(image_path, user_name)
        
        if result:
            resp_list = {}

            list = os.listdir("images\output_images\{0}".format(user_name))
            number_files = len(list)

            if number_files == 6:
                output_dir_limits = "images\output_images\{0}".format(user_name)
                get_limit_image_path1 = "images\output_images\{0}\{1}.jpg".format(user_name,"1")
                get_limit_image_path1 = ut.crop_image(output_dir=output_dir_limits, image_path=get_limit_image_path1, image_no="1")
                
                get_limit_image_path3 = "images\output_images\{0}\{1}.jpg".format(user_name,"3")
                get_limit_image_path3 = ut.crop_image(output_dir=output_dir_limits, image_path=get_limit_image_path3, image_no="3")
                
                get_limit_image_path5 = "images\output_images\{0}\{1}.jpg".format(user_name,"5")
                get_limit_image_path5 = ut.crop_image(output_dir=output_dir_limits, image_path=get_limit_image_path5, image_no="5")
                


                ll1, ul1 = ut.get_upper_lower_limits(get_limit_image_path1)
                print("---------------------------------------")
                print("ll1: ", ll1)
                print("ul1: ", ul1)
                print("---------------------------------------")
                
                ll3, ul3 = ut.get_upper_lower_limits(get_limit_image_path3)
                print("---------------------------------------")
                print("ll3: ", ll3)
                print("ul3: ", ul3)
                print("---------------------------------------")
                
                ll5, ul5 = ut.get_upper_lower_limits(get_limit_image_path5)
                print("---------------------------------------")
                print("ll5: ", ll5)
                print("ul5: ", ul5)
                print("---------------------------------------")
                
                # delete_dir = "images\output_images\{0}\cropped_images".format(user_name)
                # if os.path.isdir(delete_dir):
                #     shutil.rmtree(delete_dir)


                reaction_dir = "images\\output_images\\{0}\\reaction".format(user_name)
                if os.path.isdir(reaction_dir):
                    shutil.rmtree(reaction_dir)
                    os.mkdir(reaction_dir)
                else:
                    os.mkdir(reaction_dir)
                
                for i in range(6):
                    
                    if i in [0, 1]:
                        print("@@@@@ get ul and ll of image 0, 1 @@@@@")
                        image_path = "images\output_images\{0}\{1}.jpg".format(user_name,i)
                        resp = ut.get_saturation_pink(image_path, key, ll1, ul1, user_name)
                        
                    elif i in [2, 3]:
                        print("@@@@@ get ul and ll of image 2, 3 @@@@@")
                        image_path = "images\output_images\{0}\{1}.jpg".format(user_name,i)
                        resp = ut.get_saturation_pink(image_path, key, ll3, ul3, user_name)

                    elif i in [4, 5]:
                        print("@@@@@ get ul and ll of image 4, 5 @@@@@")
                        image_path = "images\output_images\{0}\{1}.jpg".format(user_name,i)
                        resp = ut.get_saturation_pink(image_path, key, ll5, ul5, user_name)

                    resp_list.update({
                        i: str(resp)
                    })

            else:
                resp_list = {"0": "-1", "1": "-1", "2": "-1", "3": "-1", "4": "-1", "5": "-1","message": f"Number of images are {number_files}"}

        else:
            resp_list = {"0": str(result), "1": str(result), "2": str(result), "3": str(result), "4": str(result), "5": str(result), "message": "Something is wrong with the image."}

        later = datetime.now()
        time_taken = (later - start).total_seconds()
        print("\ntime_taken", time_taken)
        print("\n", resp_list)

        return jsonify(resp_list)

    return HTML_FORM


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
