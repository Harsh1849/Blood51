import os
import shutil
import math
import cv2
import numpy as np
import pandas as pd
from detecto import core, utils, visualize


class UTILS:

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
                
                
            model = core.Model.load('model_weights.pth', ['obj_bottom','obj_mid','obj_top'])

            # Specify the path to your image
            image = utils.read_image(input_image)
            predictions = model.predict(image)

            # predictions format: (labels, boxes, scores)
            labels, boxes, scores = predictions


            thresh=0.7
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

            #print(tmp_box)
            #for box in tmp_box:
            num=1
            for box in df.values.tolist():
                x,y,w,h, hy = box
                x1=x
                y1=y
                x2=x+w
                y2=y+h

                crop_img = bgr_img[y1:y2, x1:x2]
                #index = tmp_box_original.index(box)
                #name = str(num)+"_"+filtered_labels[index]+".png"
                name = f"{output_dir}\{str(num)}.jpg"
                cv2.imwrite(name, crop_img)
                num=num+1  
            
            # visualize.show_labeled_image(image, filtered_boxes, filtered_labels)
            return True
        
        except Exception as e:
            print("@@@Error in generate images: ", e)
            return False


    def cropping(self, image_path):
        img = cv2.imread(image_path)
        height,width,_ = img.shape
        cropped_img = img[int(0.7*height):int(0.9*height), int(0.3*width):int(0.7*width)] 

        g_value =0
        i=0

        height2,width2,_ = cropped_img.shape
        result = cv2.fastNlMeansDenoisingColored(cropped_img,None,20,10,7,21)

        for y in range(height2):
            for x in range(width2):
                i=i+1
                g_value = g_value + result[y,x][1]

        return g_value/i

    
    def get_conc(self, g_value1, g_value2, g_value3):
        standard = 100
        conc = math.log(g_value1/g_value2)/math.log(g_value3/g_value2)*standard

        return conc