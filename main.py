# venv\Scripts\activate
# py main.py

import os
import shutil
from datetime import datetime

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
        BGR_key = eval(request.form['BGR_key']) 
        std_value = eval(request.form['std']) 
        print(BGR_key)

        image_path = os.path.join(UPLOAD_FOLDER, user_name + ".jpg")
        image_file.save(image_path)
        
        result = ut.generate_images(image_path, user_name)
        
        if result == "done":
            user_output_folder = "images\output_images\{0}".format(user_name)
            list = os.listdir(user_output_folder)
            number_files = len(list)

            resp_list = {}
            image_number = 1
            BGR_index = 0
            resp_index = 1
            std_index = 0
            if number_files == len(BGR_key) * 4:
                
                for i in range(len(BGR_key)):
                    if str(BGR_key[BGR_index]).lower() == "creatinine":
                        BGR_value = 0
                    elif str(BGR_key[BGR_index]).lower() == "glucose":
                        BGR_value = 1

                    g_value_1 = ut.cropping("images/output_images/{0}/{1}.jpg".format(user_name, image_number), user_output_folder, image_number, BGR_value)
                    g_value_2 = ut.cropping("images/output_images/{0}/{1}.jpg".format(user_name, image_number+1), user_output_folder, image_number+1, BGR_value)
                    g_value_3 = ut.cropping("images/output_images/{0}/{1}.jpg".format(user_name, image_number+2), user_output_folder, image_number+2, BGR_value)
                    g_value_4 = ut.cropping("images/output_images/{0}/{1}.jpg".format(user_name, image_number+3), user_output_folder, image_number+3, BGR_value)
                    conc1234 = ut.get_conc(g_value_1, g_value_2, g_value_3, g_value_4, std_value[std_index])

                    print("---------------------")
                    print("BGR_value: -> ", BGR_value)
                    print("std_value: -> ", std_value[std_index])
                    print(f"g_value_{image_number}", g_value_1)
                    print(f"g_value_{image_number+1}", g_value_2)
                    print(f"g_value_{image_number+2}", g_value_3)
                    print(f"g_value_{image_number+3}", g_value_4)
                    print("---------------------")

                    resp_list.update({str(resp_index): str(conc1234)})

                    image_number = image_number + 4
                    BGR_index = BGR_index + 1
                    resp_index = resp_index + 1
                    std_index = std_index + 1
                
            else:
                resp_list = {}
                i = 1
                for i in range(len(BGR_key)):
                    resp_list.update({str(i): "-1"})
                    i = i+1
                
                resp_list.update({"message": f"Number of images are {number_files}."})

        else:
            resp_list = {}
            i = 1
            for i in range(len(BGR_key)):
                resp_list.update({str(i): str(result)})
                i = i+1
            
            resp_list.update({"message": "Something is wrong with the image."})

        later = datetime.now()
        time_taken = (later - start).total_seconds()
        print("\n", resp_list)
        print("\ntime_taken", time_taken)

        return jsonify(resp_list)

    else:
        return HTML_FORM


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
