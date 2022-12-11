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

    
def save_record():
    global label1,label2
    if len(customer_inform)!=1:
        return
    cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='parking')
    cursor = cnx.cursor()
    add_plate = ("INSERT INTO LicensePlates "
               "(NumberPlates, Images) "
               "VALUES (%s, %s)")
    data_plate = (customer_inform[0],customer_inform[1])

    cursor.execute(add_plate, data_plate)
    cnx.commit()

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

def check_existingnumberplate(number_plate):
    cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='parking')
    cursor = cnx.cursor()
    query = ("SELECT Image FROM LicensePlates WHERE NumberPlate = %s")
    cursor.execute(query, (number_plate,))
    myresult = cursor.fetchall()
    if myresult is not None:
        if len(myresult) > 0:
            print(myresult[0])
            display_customer_img(''.join(myresult[0]))
            remove_btn['state']='normal'
            return 1
        remove_btn['state']='disable'
    return 0