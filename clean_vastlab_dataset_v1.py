#This code wrote by Ali AlShami for the Vast lab
#Clean up the dataset and choose the best detection for the subject and object
#We used Tkinter library for the GUI part
#Tkinter is a python binding to the Tk GUI toolkit
#Ali's path for the images and csv files
#C:\Users\alial\PyQt5\clean_data_v1\Triplets_exist_in_the_umd_training_data
#C:\Users\alial\PyQt5\clean_data_v1\csv_files
from tkinter import *
from PIL import ImageTk
from PIL import Image
import pandas as pd
import numpy as np
import pdb
import cv2
import os
import glob

#Input the root directry to the code
new_images_root_path  = input("Enter your image file root path: \n")
new_csv_files_root_path=input("Enter your csv files root path: \n")
sign=input("What OS you use? (Windows enter 'W', Linux enter 'L'\n")
if sign =='W' or sign =='w':
    new_sign = "\\"
elif(sign =='L' or sign =='l'):
    new_sign = "/"
else:
    print("Wrong Input for the OS Type")
    pass

index1 = int(input("Enter the index number: \n"))
print("Clearning data in progress.... ")
root = Tk()
root.title('Dataset Image')
# Dictionaries for subject, object, and verb name and ID (Based on UMD dataset)
subject_d ={"absent":-1, "person":1, "dog":2,"cat":3, "horse":4, "novel":0}
object_d  ={"absent":-1, "novel":0, "frisbee":1, "bag":2, "backpack":2, "bicycle":3, "bike":3, "motor bike":3, "bow-tie":4, "tie":4, "umbrella":5, "tv":6, "carriage":7, "horse-carriage":7, "hay":8, "dog":9,"cat":10}
verb_d    ={"novel/unknown":0, "carrying":1, "carry":1,"wearing":2, "riding":3, "ride":3, "catching":4, "catch":4, "pulling":5, "eating":6, "watching":7}

#Create folders and split the images to good images and bad detection images
if not os.path.exists("two_bb_images"):
    os.mkdir("two_bb_images")
if not os.path.exists("one_bb_images_org"):
    os.mkdir("one_bb_images_org")
if not os.path.exists("one_bb_images_bb"):
    os.mkdir("one_bb_images_bb")
if not os.path.exists("nan_bb_images"):
    os.mkdir("nan_bb_images")
if not os.path.exists("new_dataset_org"):
    os.mkdir("new_dataset_org")
if not os.path.exists("new_dataset_bb"):
    os.mkdir("new_dataset_bb")    
if not os.path.exists("bad_detection_org"):
    os.mkdir("bad_detection_org")
if not os.path.exists("bad_detection_bb"):
    os.mkdir("bad_detection_bb")

#First output directory for the images that have two bounding boxes
output_directory1 = (f"two_bb_images{new_sign}")
#Second output director for the images that have one bounding box
output_directory2 = (f"one_bb_images_org{new_sign}")
#Third output director for the images that have nan bounding box
output_directory3 = (f"nan_bb_images{new_sign}")
#Fourth output directory for our new datasets
output_directory4 = (f"new_dataset_org{new_sign}")
#Fifth directory for the bad bounding boxesclean_data_v1\
output_directory5 = (f"bad_detection_org{new_sign}")
#Add onther three folders to evaluate how good the student made the desion
output_directory6 = (f"new_dataset_bb{new_sign}")
output_directory7 = (f"bad_detection_bb{new_sign}")
output_directory8 = (f"one_bb_images_bb{new_sign}")

#Create a CSV file for the Vast labe dataset that has good bounding boxes for the subject and object
if not os.path.exists("vastdata_v1.csv"):
    output_file = open("vastdata_v1.csv",'w')
    output_file.write(f'image_path,subject_name,subject_id,object_name,object_id,verb_name,verb_id,image_width,image_height,subject_ymin,subject_xmin,subject_ymax,subject_xmax,object_ymin,object_xmin,object_ymax,object_xmax\n')
else:
    output_file = open("vastdata_v1.csv",'a')
#Create a CSV file for the bad bounding boxes
if not os.path.exists("bad_bb_v1.csv"):
    output_file1 = open("bad_bb_v1.csv",'w')
    output_file1.write(f'image_path,subject_name,subject_id,object_name,object_id,verb_name,verb_id,image_width,image_height,subject_ymin,subject_xmin,subject_ymax,subject_xmax,object_ymin,object_xmin,object_ymax,object_xmax\n')
else:
    output_file1 = open("bad_bb_v1.csv",'a')
#Create a CSV file for the one boudning boxes images
if not os.path.exists("one_bb_v1.csv"):
    output_file2 = open("one_bb_v1.csv",'w')
    output_file2.write(f'image_path,subject_name,subject_id,object_name,object_id,verb_name,verb_id,image_width,image_height,subject_ymin,subject_xmin,subject_ymax,subject_xmax,object_ymin,object_xmin,object_ymax,object_xmax\n')
else:
    output_file2 = open("one_bb_v1.csv",'a')

all_csv_files = glob.glob(new_csv_files_root_path+new_sign+"*.csv")
#pdb.set_trace()
#Go through all the CSV files that have the coordinates of the boudnign boxs
for csv_file in all_csv_files:
    svo_names = csv_file.split(new_sign)
    #Take the name of the subject, object, and verb from the CSV file
    subject_name, verb_name, object_name, det = svo_names[-1].split("_")
    # Get the Subject, Object, and Verb ID based on UMD
    for key, value in subject_d.items():
        if subject_name == key:
            subject_id = []
            subject_id = value
    for key, value in verb_d.items():
        if verb_name == key:
            verb_id = []
            verb_id = value
    for key, value in object_d.items():
        if object_name == key:
            object_id = []
            object_id = value
    
    #print(f'The subject_name {subject_name} the vern_name {verb_name} the object_name {object_name}')
    #print(f'The subject_id {subject_id} the vern_id {verb_id} the object_id{object_id}')
    df = pd.read_csv(csv_file, index_col = None)
    for index, row in df.iterrows():
        index1+=1
        csv_address      = row["image_path"]
        image_name = csv_address.split("/")
        image_name = image_name[-1]
        #If you use window, you don't have to change it. Otherwise, you need to change "\\" to "/"
        address  = (f'{new_images_root_path}{new_sign}{subject_name}_{verb_name}_{object_name}{new_sign}{image_name}')
        #print(f'new_address {address}')
        subject_ymin = row["subject_box_y1"]
        subject_xmin = row["subject_box_x1"]
        subject_ymax = row["subject_box_y2"]
        subject_xmax = row["subject_box_x2"]
        object_ymin  = row["object_box_y1"]
        object_xmin  = row["object_box_x1"]
        object_ymax  = row["object_box_y2"]
        object_xmax  = row["object_box_x2"]
        subject_count= row["subject_count"]
        object_count = row["object_count"]
        # Convert the float numbers to int
        subject_ymin = round(subject_ymin)
        subject_xmin = round(subject_xmin)
        subject_ymax = round(subject_ymax)
        subject_xmax = round(subject_xmax)
        object_ymin  = round(object_ymin)
        object_xmin  = round(object_xmin)
        object_ymax  = round(object_ymax)
        object_xmax  = round(object_xmax)
        #Read the Image
        org_img  = cv2.imread(address, 1)
        img      = org_img
        height   = img.shape[0]
        width    = img.shape[1]
        channels = img.shape[2]

        #Used assert to not raise an error
        assert subject_xmin <= subject_xmax
        assert subject_xmax <= width
        assert object_xmin <= object_xmax
        assert object_xmax <= width
        assert subject_ymin <= subject_ymax
        assert subject_ymax <= height
        assert object_ymin <= object_ymax
        assert object_ymax <= height

        #Add boudning box for the Subject
        if (subject_xmax >=0) or (subject_ymax >=0):
          subject_xmin = max(0,subject_xmin)
          subject_xmax = max(0,subject_xmax)
          subject_ymin = max(0,subject_ymin)
          subject_ymax = max(0,subject_ymax)
          im_1 = cv2.rectangle(img, (subject_xmin,subject_ymin), (subject_xmax,subject_ymax), (0,0,255), 3)
          cv2.putText(im_1,subject_name, (subject_xmin,subject_ymin-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        else:
          im_1 = img
        #Add bounding box for the Object
        if (object_xmax >=0) or (object_ymax >=0):
          object_xmin = max(0,object_xmin)
          object_xmax = max(0,object_xmax)
          object_ymin = max(0,object_ymin)
          object_ymax = max(0,object_ymax)
          image = cv2.rectangle(im_1, (object_xmin,object_ymin), (object_xmax,object_ymax), (0,255,0), 3)
          cv2.putText(image, object_name, (object_xmin,object_ymin-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        else:
          image = im_1

        filename = str(index1)
        text_1 = f"<{subject_name},{verb_name},{object_name}>"
        org_1 = (10, 50)
        image = cv2.putText(image, text_1, org_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        #The GUI using Tkinter to see the image with that has bounding box for the subject and object 
        if (subject_count > 0) and (object_count > 0):
            path_1 = output_directory1+filename+'.jpg'
            cv2.imwrite(path_1, org_img)
            imgs = Image.fromarray(image)
            if width > 500 or height > 500:
                imgs = imgs.resize((500,500))
                imgs = ImageTk.PhotoImage(imgs)
            else:
                imgs = ImageTk.PhotoImage(imgs)
            label = Label(image=imgs, height=500,width=500)
            label.grid(row=0, column=0, columnspan=3)
            running = True  # Global flag
            #Forward function for the Keep the image button
            def forward():
                path_4 = output_directory4+filename+'.jpg'
                path_6 = output_directory6+filename+'.jpg'
                print(path_4)
                cv2.imwrite(path_6, org_img)
                org_img1  = cv2.imread(address, 1)
                cv2.imwrite(path_4, org_img1)
                output_file.write(f'{path_4},{subject_name},{subject_id},{object_name},{object_id},{verb_name},{verb_id},{width},{height},{subject_ymin},{subject_xmin},{subject_ymax},{subject_xmax},{object_ymin},{object_xmin},{object_ymax},{object_xmax}\n')
                root.quit()
            #Ignore function for the Ignore the image button
            def Ignore():
                path_5 = output_directory5+filename+'.jpg'
                path_7 = output_directory7+filename+'.jpg'
                cv2.imwrite(path_7, org_img)
                org_img2 = cv2.imread(address, 1)
                cv2.imwrite(path_5, org_img2)
                output_file1.write(f'{path_5},{subject_name},{subject_id},{object_name},{object_id},{verb_name},{verb_id},{width},{height},{subject_ymin},{subject_xmin},{subject_ymax},{subject_xmax},{object_ymin},{object_xmin},{object_ymax},{object_xmax}\n')
                root.quit()

            button_back    = Button(root, text="Ignore the image",command=lambda:Ignore())
            button_forward = Button(root, text="Keep the image"  ,command=lambda:forward())
            button_back.grid(row=1, column=0)
            button_forward.grid(row=1, column=2)
            root.mainloop()
        #Move the image with one bounding box for a folder
        elif(subject_count == -1) and (object_count > 0):
            path_2 = output_directory2+filename+'.jpg'
            cv2.imwrite(path_2, org_img)
            path_8 = output_directory8+filename+'.jpg'
            org_img3 = cv2.imread(address, 1)
            cv2.imwrite(path_8, org_img3)
            output_file2.write(f'{path_8},{subject_name},{subject_id},{object_name},{object_id},{verb_name},{verb_id},{width},{height},{subject_ymin},{subject_xmin},{subject_ymax},{subject_xmax},{object_ymin},{object_xmin},{object_ymax},{object_xmax}\n')
        elif(subject_count > 0) and (object_count == -1):
            path_2 = output_directory2+filename+'.jpg'
            cv2.imwrite(path_2, org_img)
            path_8 = output_directory8+filename+'.jpg'
            org_img3 = cv2.imread(address, 1)
            cv2.imwrite(path_8, org_img3)
            output_file2.write(f'{path_8},{subject_name},{subject_id},{object_name},{object_id},{verb_name},{verb_id},{width},{height},{subject_ymin},{subject_xmin},{subject_ymax},{subject_xmax},{object_ymin},{object_xmin},{object_ymax},{object_xmax}\n')
        #Move the image with nan boudning box for a folder
        else:
            path_3 = output_directory3+filename+'.jpg'
            cv2.imwrite(path_3, org_img)
print(f"The index number is: {index1}")
output_file.close()
