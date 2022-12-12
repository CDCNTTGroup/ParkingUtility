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
    
def save_record():
    global label1,label2, label_existing_check,label_number_plate
    if len(customer_inform)!=2:
        return
    cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='parking')
    cursor = cnx.cursor()
    add_plate = ("INSERT INTO LicensePlates "
               "(NumberPlate, Image) "
               "VALUES (%s, %s)")
    data_plate = (customer_inform[0],customer_inform[1])

    cursor.execute(add_plate, data_plate)
    cnx.commit()
    
    label1.config(image='')
    label2.config(image='')
    label_existing_check.config(text='')
    label_number_plate.config(text='')
    return
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

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

def readnumberplate(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) #Edge detection
    plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
    
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break
    
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0,255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    
    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]
        
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    
    t=result[0][1]+result[1][1]
    return t
    
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

def upload_customerfile_entrance():
    global customer_inform
    if len(customer_inform)==0:
        return
    if len(customer_inform)==1: 
        save_btn['state']='disable'
        
    file = askopenfile(mode='r', filetypes=[('Image Files',  ['.jpeg', '.jpg', '.png', '.gif',
                                                       '.tiff', '.tif', '.bmp'])])
    if not file:
            return None
    dir_ = file.name
    
    customer_inform.append(dir_)
    display_customer_img(dir_)
    # img_ =Image.open(dir_)
    
    # img_ =cv2.imread(dir_)
    # RGB_img = cv2.cvtColor(img_, cv2.COLOR_BGR2RGB)
    # img_=image_resize(RGB_img,width=300)
    # img = ImageTk.PhotoImage(Image.fromarray(img_))
    
    # label1 = Label(image=img)
    # label1.image = img
    
    # label1.place(x=550,y=175, width = 300, height=300)
    print(customer_inform)
    
    if len(customer_inform)==2:
        save_btn['state']='normal'
        
        
    return

app = Tk()

app.geometry("894x900")
app.configure(bg = "#FFFFFF")
canvas = Canvas(
    app,
    bg = "#FFFFFF",
    height = 600,
    width = 900,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
label1 = Label(image='')
label2= Label(image='')
file_upload_btn = Button(app, text="Upload Number Plate Image",
                                 command=lambda: upload_file_entrance())
file_upload_btn.place(
    x=50,
    y=100,
    width=200.0,
    height=40.0
)

file_upload_btn_2 = Button(app, text="Upload Customer Image",
                                 command=lambda: upload_customerfile_entrance())
file_upload_btn_2.place(
    x=550,
    y=100,
    width=200.0,
    height=40.0
)
save_btn= Button(app, text="Save",
                                    command=lambda: save_record())
save_btn.place(
            x=550,
            y=575,
            width=150.0,
            height=56.0
        )
save_btn['state']="disable"

remove_btn = Button(app, text="Remove Number Plate", command=lambda: remove_record())
remove_btn.place(x=190,y=575,width=150,height=56)
remove_btn['state']="disable"


app.resizable(False, False)
app.mainloop()