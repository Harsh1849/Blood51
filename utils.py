import os
import shutil

import cv2
import numpy as np
import pandas as pd
from detecto import core, utils, visualize


class UTILS:
    
    def get_saturation_pink(self, image_path, key, LL, UL, user_name):    
        try:
            if os.path.isfile(image_path):


                saturation_pink = 0
                saturation_red = 0

                img = cv2.imread(image_path)

                width,height,_ = img.shape

                result = cv2.fastNlMeansDenoisingColored(img,None,20,10,7,21)

                hsv_img = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
                #cv2.imshow("HSV Image", hsv_img)


                lower_pink = np.array(LL)
                upper_pink = np.array(UL)

                print("saturation_pink func", lower_pink)
                print("saturation_pink func", upper_pink)


                masking = cv2.inRange(hsv_img, lower_pink, upper_pink)
                #cv2.imshow("pink Color detection", masking)
                result_pink = cv2.bitwise_and(img, img, mask=masking)

                # half_pink = cv2.resize(result_pink, (0, 0), fx = 0.1, fy = 0.1) #resizing the image
                # cv2.imshow("Reacted area - pink", result_pink)
                               
                reaction_dir = "images\\output_images\\{0}\\reaction".format(user_name)
                os.path.join(reaction_dir, "Reacted0.jpg")
                if not os.path.exists(os.path.join(reaction_dir, "Reacted0.jpg")):
                    cv2.imwrite(os.path.join(reaction_dir, "Reacted0.jpg"), result_pink)

                elif not os.path.exists(os.path.join(reaction_dir, "Reacted1.jpg")):
                    cv2.imwrite(os.path.join(reaction_dir, "Reacted1.jpg"), result_pink)

                elif not os.path.exists(os.path.join(reaction_dir, "Reacted2.jpg")):
                    cv2.imwrite(os.path.join(reaction_dir, "Reacted2.jpg"), result_pink)

                elif not os.path.exists(os.path.join(reaction_dir, "Reacted3.jpg")):
                    cv2.imwrite(os.path.join(reaction_dir, "Reacted3.jpg"), result_pink)

                elif not os.path.exists(os.path.join(reaction_dir, "Reacted4.jpg")):
                    cv2.imwrite(os.path.join(reaction_dir, "Reacted4.jpg"), result_pink)

                elif not os.path.exists(os.path.join(reaction_dir, "Reacted5.jpg")):
                    cv2.imwrite(os.path.join(reaction_dir, "Reacted5.jpg"), result_pink)


                for x in range(width):
                    for y in range(height):
                        saturation_pink = saturation_pink + result_pink[x,y][1]*result_pink[x,y][0]#*(50 - result_pink[x,y][0])

                print("pink saturation : ",saturation_pink)
                cv2.waitKey(1)

            else:
                print(f"No image generated at {image_path}")
                saturation_pink = -1

        except Exception as e:
            print("@@@",e)
            saturation_pink = 0    
            
        return str(saturation_pink)
            
    def generate_images(self, input_image, input_image_name):
        
        try:
            
            parent_dir = "images\output_images"
            if not os.path.isdir(parent_dir):
                os.mkdir(parent_dir)

            output_dir = os.path.join(parent_dir, input_image_name)

            if os.path.isdir(output_dir):
                print("dir exists...")
                shutil.rmtree(output_dir)
                os.mkdir(output_dir)
            else:
                os.mkdir(output_dir)
                
                
            model = core.Model.load('model_weights.pth', ['obj_bottom', 'obj_top'])

            # Specify the path to your image
            image = utils.read_image(input_image)
            cv2.imread(input_image)
            predictions = model.predict(image)

            # predictions format: (labels, boxes, scores)
            labels, boxes, scores = predictions


            thresh=0.8
            filtered_indices=np.where(scores>thresh)
            filtered_scores=scores[filtered_indices]
            filtered_boxes=boxes[filtered_indices]
            num_list = filtered_indices[0].tolist()
            filtered_labels = [labels[i] for i in num_list]
            bgr_img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #for opencv
            i=0

            #sort box in top left to bottom right order.
            #tmp_box = []
            #tmp_box_original = []
            #for box in filtered_boxes:
            #	tmp_box.append([int(box[0]),int(box[1]),int(box[2])-int(box[0]),int(box[3])-int(box[1])])
            #	tmp_box_original.append([int(box[0]),int(box[1]),int(box[2])-int(box[0]),int(box[3])-int(box[1])])

            #tmp_box_np = np.array(tmp_box)
            #max_height = np.max(tmp_box_np[::, 3])
            #nearest = max_height * 1.4
            #tmp_box.sort(key=lambda r: [int(nearest * round(float(r[1]) / nearest)), r[0]])

            bboxes = []
            for box in filtered_boxes:
                bboxes.append([int(box[0]),int(box[1]),int(box[2])-int(box[0]),int(box[3])-int(box[1])])
            bboxes=sorted(bboxes, key=lambda x: x[0])

            df=pd.DataFrame(bboxes, columns=['x','y','w', 'h'], dtype=int)
            df["x2"] = df["x"]+df["w"] # adding column for x on the right side
            df = df.sort_values(["x","y", "x2"]) # sorting

            for i in range(2): # change rows between each other by their coordinates several times 
            # to sort them completely 
                for ind in range(len(df)-1):
                #     print(ind, df.iloc[ind][4] > df.iloc[ind+1][0])
                    if df.iloc[ind][4] > df.iloc[ind+1][0] and df.iloc[ind][1]> df.iloc[ind+1][1]:
                        df.iloc[ind], df.iloc[ind+1] = df.iloc[ind+1].copy(), df.iloc[ind].copy()

            # print(df)
            #for box in tmp_box:
            num=0
            for box in df.values.tolist():
                x,y,w,h, hy = box
                x1=x
                y1=y
                x2=x+w
                y2=y+h


                start_point = (x1,y1)
                end_point = (x2,y2)
                color = (255, 0, 0)
                tmp_img = cv2.rectangle(bgr_img.copy(), start_point, end_point, color, 2)
                cv2.namedWindow("window_name", cv2.WINDOW_NORMAL) 
                # cv2.imshow("window_name", tmp_img)
                cv2.waitKey(1)
                
                crop_img = bgr_img[y1:y2, x1:x2]
                #index = tmp_box_original.index(box)
                #name = str(num)+"_"+filtered_labels[index]+".png"
                    
                # name = str(num)+".png"
                name = f"{output_dir}\{str(num)}.jpg"
                cv2.imwrite(name, crop_img)
                num=num+1  
            
            # visualize.show_labeled_image(image, filtered_boxes, filtered_labels)
            return True
        
        except Exception as e:
            print(e)
            return False
      
    def crop_image(self, output_dir, image_path, image_no):
        img = cv2.imread(image_path)

        height,width,_ = img.shape

        cropped_img = img[int(0.7*height):int(0.9*height), int(0.2*width):int(0.8*width)] 

        output_dir = os.path.join(output_dir, "cropped_images")
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        else:
            print("dir exists...")
            
        name = f"{output_dir}\{str(image_no)}.jpg"
        cv2.imwrite(name, cropped_img)
        
        return name

    def get_upper_lower_limits(self, image_path):
        
        min_s = 30
        min_h = 255
        max_h = 0

        img = cv2.imread(image_path)

        height,width,_ = img.shape

        result = cv2.fastNlMeansDenoisingColored(img,None,20,10,7,21)

        hsv_img = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
        #cv2.imshow("HSV Image", hsv_img)

        for x in range(width):
            for y in range(height):

                if (hsv_img[y,x][1] < min_s):
                    min_s = hsv_img[y,x][1]

                if (hsv_img[y,x][0] < min_h):
                    min_h = hsv_img[y,x][0]

                if (hsv_img[y,x][0] > max_h):
                    max_h = hsv_img[y,x][0]


        lower_limit = np.array([min_h, min_s, 0])
        upper_limit = np.array([max_h, 255, 255])
        

        print("---------------------------------------")
        print(image_path)
        print("lower limit : ",lower_limit)
        print("upper limit : ",upper_limit)
        print("---------------------------------------")

        cv2.waitKey(1)
        
        return lower_limit, upper_limit
