from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
from tkinter import ttk
from PIL import ImageTk, Image
import os
import numpy as np
from matplotlib.image import imread
import matplotlib.pyplot as plt
import cv2
import imutils
from math import hypot


def BrowsePic():
    global panelA, panelB, panelC, panelD, panelE, panelF

    path = filedialog.askopenfilename()

    if len(path) > 0:
        img = cv2.imread(path)
        img = imutils.resize(img, width=300)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        kernel = np.ones((5, 5), np.float32)/25
        imgfiltered = cv2.filter2D(gray, -1, kernel)

        kernelOp = np.ones((10, 10), np.uint8)
        kernelCl = np.ones((15, 15), np.uint8)

        ret, thresh_image = cv2.threshold(
            imgfiltered, 100, 255, cv2.THRESH_BINARY)

        morpho = cv2.morphologyEx(thresh_image, cv2.MORPH_OPEN, kernelOp)
        circles = cv2.HoughCircles(
            morpho, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
        cimg_morpho = img.copy()
        img_morpho_copy = morpho.copy()

        if circles is not None:
            circle_values_list = np.uint16(np.around(circles))
            x, y, r = circle_values_list[0, :][0]

            rows, cols = img_morpho_copy.shape

            for i in range(cols):
                for j in range(rows):
                    if hypot(i-x, j-y) > r:
                        img_morpho_copy[j, i] = 0

        imgg_inv = cv2.bitwise_not(img_morpho_copy)
        contours0, hierarchy = cv2.findContours(
            img_morpho_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cimg_pupil = img.copy()

        for cnt in contours0:
            cv2.drawContours(cimg_pupil, cnt, -1, (0, 255, 0), 3, 8)
            pupil_area = cv2.contourArea(cnt)
            label6 = Label(FrameKl, text="Pupil area: %d" % pupil_area)

        contours0, hierarchy = cv2.findContours(
            imgg_inv, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        cimg_cat = img.copy()

        for cnt in contours0:
            if cv2.contourArea(cnt) < pupil_area:

                cv2.drawContours(cimg_cat, cnt, -1, (0, 255, 0), 3, 8)
                cat_area = cv2.contourArea(cnt)

                cataract_percentage = (
                    cat_area / (pupil_area + cat_area)) * 100

                label1 = Label(FrameKl, text="Area Katarak: %d" % (cat_area))
                label4 = Label(
                    FrameKl, text="Anda punya %.2f persen katarak" % (cataract_percentage))

                # label6.pack()
                # label1.pack()
                # label4.pack()

    m = cv2.meanStdDev(gray)

    if m[0] < 50:
        sehat1 = Label(FrameKl, text='Tidak ada katarak')
        sehat2 = Label(FrameKl, text='Mata Sehat')
        sehat1.place(relx=0.5, y=30, anchor=CENTER)
        sehat2.place(relx=0.5, y=60, anchor=CENTER)
    elif m[0] <= 100:
        ringan1 = Label(FrameKl, text='Adanya Katarak')
        ringan2 = Label(FrameKl, text='Mata memiliki katarak ringan')
        ringan1.place(relx=0.5, y=30, anchor=CENTER)
        ringan2.place(relx=0.5, y=60, anchor=CENTER)
    else:
        parah1 = Label(FrameKl, text='Adanya Katarak')
        parah2 = Label(FrameKl, text='Mata memiliki katarak parah')
        parah1.place(relx=0.5, y=30, anchor=CENTER)
        parah2.place(relx=0.5, y=60, anchor=CENTER)

#         print('Mean:', m[0])

#         plt.hist(gray.ravel(), 256, [0, 256])
#         plt.axvline(gray.mean(), color='k', linestyle='dashed', linewidth=1)
#         plt.show()

        cv2.waitKey(0)

        img = Image.fromarray(img)
        gray = Image.fromarray(gray)
        imgfiltered = Image.fromarray(imgfiltered)
        thresh_image = Image.fromarray(thresh_image)
        morpho = Image.fromarray(morpho)
        imgg_inv = Image.fromarray(imgg_inv)
        cimg_cat = Image.fromarray(cimg_cat)

        width = 300
        height = 300
        img = img.resize((width, height), Image.ANTIALIAS)
        gray = gray.resize((width, height), Image.ANTIALIAS)
        imgfiltered = imgfiltered.resize((width, height), Image.ANTIALIAS)
        thresh_image = thresh_image.resize((width, height), Image.ANTIALIAS)
        morpho = morpho.resize((width, height), Image.ANTIALIAS)
        imgg_inv = imgg_inv.resize((width, height), Image.ANTIALIAS)
        cimg_cat = cimg_cat.resize((width, height), Image.ANTIALIAS)

        img = ImageTk.PhotoImage(img)
        gray = ImageTk.PhotoImage(gray)
        imgfiltered = ImageTk.PhotoImage(imgfiltered)
        thresh_image = ImageTk.PhotoImage(thresh_image)
        morpho = ImageTk.PhotoImage(morpho)
        imgg_inv = ImageTk.PhotoImage(imgg_inv)
        cimg_cat = ImageTk.PhotoImage(cimg_cat)

        if panelA is None or panelB is None or panelC is None or panelD is None or panelE is None or panelF is None:
            panelA = Label(OriFrame, image=img)
            panelA.image = img
            panelA.place(x=0, y=0)

            panelB = Label(GrayFrame, image=gray)
            panelB.image = gray
            panelB.place(x=0, y=0)

            panelC = Label(MaskFrame, image=imgfiltered)
            panelC.image = imgfiltered
            panelC.place(x=0, y=0)

            panelD = Label(BinFrame, image=thresh_image)
            panelD.image = thresh_image
            panelD.place(x=0, y=0)

            panelE = Label(CircleFrame, image=cimg_cat)
            panelE.image = cimg_cat
            panelE.place(x=0, y=0)

            panelF = Label(HistoFrame, image=morpho)
            panelF.image = morpho
            panelF.place(x=0, y=0)

        else:
            panelA.configure(image=img)
            panelB.configure(image=gray)
            panelC.configure(image=imgfiltered)
            panelD.configure(image=thresh_image)
            panelE.configure(image=cimg_cat)
            panelF.configure(image=morpho)

            panelA.image = img
            panelB.image = gray
            panelC.image = imgfiltered
            panelD.image = thresh_image
            panelE.image = cimg_cat
            panelF.image = morpho


root = Tk()
panelA = None
panelB = None
panelC = None
panelD = None
panelE = None
panelF = None


style = ttk.Style(root)
root.tk.call('source', 'azure/azure.tcl')
style.theme_use('azure')
style.configure("Accentbutton", foreground='white')

window_height = 800
window_width = 1300
# 1350

# Window


def center_screen():
    """ gets the coordinates of the center of the screen """
    global screen_height, screen_width, x_cordinate, y_cordinate

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    root.geometry("{}x{}+{}+{}".format(window_width,
                                       window_height, x_cordinate, y_cordinate))


center_screen()


# Label
Judul = Label(root, text='Segmentasi Citra Mata Katarak', font=('arial', 24))
Judul.place(relx=0.5, y=20, anchor=CENTER)

# Frame
FrameOp = ttk.LabelFrame(root, text='Operation', width=200, height=165)
FrameOp.place(x=20, y=100)

FrameKl = ttk.LabelFrame(root, text='Klasifikasi', width=200, height=125)
FrameKl.place(x=20, y=290)

# Buttons
BrImg = ttk.Button(FrameOp, text="Browse Image", style='Accentbutton')
BrImg['command'] = BrowsePic
BrImg.place(relx=0.5, y=30, anchor=CENTER)

GrImg = ttk.Button(FrameOp, text="Graphics", style='Accentbutton')
# GrImg['command'] = Grafik
GrImg.place(relx=0.5, y=70, anchor=CENTER)
# ProcImg = ttk.Button(root, text="Process Image", style='Accentbutton')
# ProcImg['command'] = ProcessPic
# # ProcImg.place(x=20, y=60)
# ProcImg.place(x=20, y=280)  # Luar Frame

RstImg = ttk.Button(FrameOp, text="Reset", style='Accentbutton')
# RstImg.place(x=20, y=100)
RstImg.place(relx=0.5, y=110, anchor=CENTER)  # Luar Frame

# Notebook Image
OriBook = ttk.Notebook(root)
OriFrame = ttk.Frame(OriBook, width=300, height=300)
OriBook.add(OriFrame, text='Original Image')
OriBook.place(x=250, y=60)

Graybook = ttk.Notebook(root)
GrayFrame = ttk.Frame(Graybook, width=300, height=300)
Graybook.add(GrayFrame, text='Grayscale Image')
Graybook.place(x=250, y=410)

Binbook = ttk.Notebook(root)
BinFrame = ttk.Frame(Binbook, width=300, height=300)
Binbook.add(BinFrame, text='Binary Image')
Binbook.place(x=600, y=410)

Maskbook = ttk.Notebook(root)
MaskFrame = ttk.Frame(Maskbook, width=300, height=300)
Maskbook.add(MaskFrame, text='Filtered Image')
Maskbook.place(x=600, y=60)

Circlebook = ttk.Notebook(root)
CircleFrame = ttk.Frame(Circlebook, width=300, height=300)
Circlebook.add(CircleFrame, text='Circle Detection Image')
Circlebook.place(x=950, y=60)

Histobook = ttk.Notebook(root)
HistoFrame = ttk.Frame(Histobook, width=300, height=300)
Histobook.add(HistoFrame, text='Morfologi')
Histobook.place(x=950, y=410)

root.mainloop()
