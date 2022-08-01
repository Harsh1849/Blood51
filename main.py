# venv\Scripts\activate
# py main.py

import os

import requests
from flask import Flask, jsonify, request
from sqlalchemy import null

from utils import UTILS

app = Flask(__name__)


@app.route("/api/brightness", methods=["GET", "POST"])
def get_img_brightness():


    print("brightness API call...")
    
    ut = UTILS()

    UPLOAD_FOLDER = "images\input_images"

    if request.method == "POST":

        key = request.form['key']
        user_name = request.form['user']
        
        if "image_file" in request.files:
            image_file = request.files['image_file']
            image_path = os.path.join(UPLOAD_FOLDER, user_name + ".jpg")
            # image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
            image_file.save(image_path)
        elif "image_file" in request.form:
            image_path = request.form['image_file']
        else:
            return "there is no image_file in form!"
            

        # print('@@@',image_path)
        # print('@@@',key)
        # print('@@@',user_name)

        brightness_pink = ut.Get_brightness(image_path, key)
        
        return str(brightness_pink)

    return """
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
    

@app.route("/api/detect_images", methods=["GET", "POST"])
def detect_images():
    
    ut = UTILS()

    UPLOAD_FOLDER = "images\input_images"

    if request.method == "POST":
        if "image_file" not in request.files:
            return "There is no image_file in form!"

        image_file = request.files['image_file']
        user_name = request.form['user']
        key = request.form['key']

        image_path = os.path.join(UPLOAD_FOLDER, user_name + ".jpg")
        # image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
        image_file.save(image_path)
    
        # print('@@@',image_path)
        # print('@@@',image_file)
        # print('@@@',user_name)

        
        result = ut.Generate_images(image_path, user_name)
        
        if result:
            resp_list = {}
            for i in range(6):

                list = os.listdir("images\output_images\{0}".format(user_name))
                number_files = len(list)

                if number_files == 6:

                    image_path = "images\output_images\{0}\{1}.jpg".format(user_name,i)

                    payload = {
                        "image_file": image_path,
                        "key": key,
                        "user": user_name
                    }
                    
                    resp = requests.post(f"http://127.0.0.1:8000/api/brightness", data=payload)

                    resp_list.update({
                        i : resp.content.decode("utf-8")
                    })
                                            
                else:
                    resp_list = {"0": "-1", "1": "-1", "2": "-1", "3": "-1", "4": "-1", "5": "-1","message": f"Number of images are {number_files}"}

        else:
            resp_list = {"0": str(result), "1": str(result), "2": str(result), "3": str(result), "4": str(result), "5": str(result), "message": "Something is wrong with the image."}

        print(resp_list)


        return jsonify(resp_list)


    return """
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
