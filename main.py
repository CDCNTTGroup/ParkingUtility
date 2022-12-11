from PIL import ImageTk, Image
import mysql.connector
import easyocr
import imutils
import numpy as np
from matplotlib import pyplot as plt
import cv2
from tkinter import *
from tkinter.filedialog import askopenfile
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


customer_inform = []


def remove_record():
    global label1, label2
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='parking')
    cursor = cnx.cursor()
    remove_plate = ("DELETE FROM LicensePlates WHERE NumberPlate = %s")

    data_plate = (customer_inform[0],)

    cursor.execute(remove_plate, data_plate)
    cnx.commit()

    label1.config(image='')
    label2.config(image='')
    return


def save_record():
    global label1, label2
    if len(customer_inform) != 1:
        return
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='parking')
    cursor = cnx.cursor()
    add_plate = ("INSERT INTO LicensePlates "
                 "(NumberPlates, Images) "
                 "VALUES (%s, %s)")
    data_plate = (customer_inform[0], customer_inform[1])

    cursor.execute(add_plate, data_plate)
    cnx.commit()

    return


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=inter)

    return resized


def display_customer_img(dir_):
    global label2
    img_ = cv2.imread(dir_)
    RGB_img = cv2.cvtColor(img_, cv2.COLOR_BGR2RGB)
    img_ = image_resize(RGB_img, width=300)
    img = ImageTk.PhotoImage(Image.fromarray(img_))

    label2.config(image=img)
    label2.image = img

    label2.place(x=550, y=175, width=300, height=300)
    
def upload_file_entrance():
    global label1
    global customer_inform 
    customer_inform = []
    save_btn['state']='disable'
    file = askopenfile(mode='r', filetypes=[('Image Files',  ['.jpeg', '.jpg', '.png', '.gif',
                                                       '.tiff', '.tif', '.bmp'])])
    if not file:
            return None
        
    dir_ = file.name
    result = readnumberplate(dir_)
    
    customer_inform.append(result) 
    
    img_ =Image.open(dir_)
    img = ImageTk.PhotoImage(img_)
    label1 = Label(image=img)
    label1.image = img
    label1.place(x=50,y=175, width = 300, height=300)
    
    label2=Label(app, text="Number plate:"+result, font='Helvetica 18 bold')
    label2.place(x=50,y=500)
    
    existing = check_existingnumberplate(result)
    if existing == 1: 
        label_existing_check = Label(app, text='This number plate already exists',fg='red')
    else:
        label_existing_check = Label(app, text='Complete parking form with customer image',fg='red')
    
    label_existing_check.place(x=50,y=530)
        
	
    
    return 
