from tkinter import *
from tkinter.filedialog import askopenfile 
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils

import easyocr
import mysql.connector
from PIL import ImageTk,Image

customer_inform=[]

def remove_record():
    global label1, label2
    cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='parking')
    cursor = cnx.cursor()
    remove_plate=("DELETE FROM LicensePlates WHERE NumberPlate = %s")
    
    data_plate=(customer_inform[0],)
    
    cursor.execute(remove_plate,data_plate)
    cnx.commit()
    
    label1.config(image='')
    label2.config(image='')
    return



def display_customer_img(dir_):
    global label2
    img_ =cv2.imread(dir_)
    RGB_img = cv2.cvtColor(img_, cv2.COLOR_BGR2RGB)
    img_=image_resize(RGB_img,width=300)
    img = ImageTk.PhotoImage(Image.fromarray(img_))
    
    label2.config(image=img)
    label2.image = img
    
    label2.place(x=550,y=175, width = 300, height=300)