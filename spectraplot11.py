import sys
import tkinter
import pandas as pd
import matplotlib
import numpy as np
from numpy import convolve
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import re
from statistics import mean

def moav (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, "same")
    return sma

def moav_exp (values, window, degree):
    weights = np.repeat(1.0, window)
    for i in range(len(weights)) :
        weights[i]=np.exp(-i*degree)
    weights = weights/sum(weights)
    sma = np.convolve(values, weights, "same")
    return sma
#right clic#
def make_menu(w):
    global the_menu
    the_menu = tkinter.Menu(w, tearoff=0)
    the_menu.add_command(label="cut")
    the_menu.add_command(label="copy")
    the_menu.add_command(label="paste")

def show_menu(e):
    w = e.widget
    the_menu.entryconfigure("cut", command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("copy", command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("paste", command=lambda: w.event_generate("<<Paste>>"))
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)
#right click
def ButtonEvent(event):
    dirofdata = EditBox_path.get()
    if Val_path.get() == True:
        path = os.path.dirname(os.path.abspath(__file__))+"\\"+dirofdata
    else:
        path = EditBox_path.get()

    list = os.listdir(path)

    list0=sorted(list, key=lambda s: int(re.search(r'(\d+)min', s).groups()[0]))

    noffile = len(list0)
    tstepc = EditBox_time.get()
    tstep = int(tstepc)
    Chc = EditBox_gas.get()
    Ch = int(Chc)-1
    mac = EditBox_N.get()
    ma = int(mac)

    if Val_z.get() == True:
        zlimminc = EditBox_zmin.get()
        zlimmin = float(zlimminc)
        zlimmaxc = EditBox_zmax.get()
        zlimmax = float(zlimmaxc)
    else:
        pass

    ylist = [ i*tstep for i in range(noffile) ]
    xlist = [ i for i in range(500) ]
    #print(xlist,ylist)
    data=[]
    ColNum = 3*Ch+2
    for filename in list0:
        filepath = path+"\\"+filename
        #print(filepath)
        csvdata = pd.read_csv(filepath, header=None)
        databf=np.array(csvdata.values[0:500,ColNum])
        #print(databf)
        databf=databf-mean(databf)
        if Val_ma.get() == False:
            degc=EditBox_decay.get()
            deg=float(degc)
            databf = moav_exp(databf,ma,deg)
        else:
            databf = moav(databf,ma)
        data.append(databf)

    X, Y = np.meshgrid(np.array(xlist), np.array(ylist))
    Z = np.array(data)
    fig = plt.figure(figsize=(6,4))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel("data points")
    ax.set_ylabel("time (min)")
    ax.set_zlabel("abs")

    if Val_z.get() == True:
        ax.set_zlim3d(zlimmin,zlimmax)
    else:
        pass

    if Val_wireframe.get() == False:
        surf = ax.plot_surface(X, Y, Z, cmap='viridis',shade=False, antialiased=False, linewidth=1)
        fig.colorbar(surf)
        fig.show()
    else:
        ax.plot_wireframe(X, Y, Z, color='blue',linewidth=0.2)
        fig.show()

root = tkinter.Tk()
root.title("Spectra Plot")
root.geometry("400x460")

make_menu(root)
root.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)

Val_path = tkinter.BooleanVar()
Val_path.set(True)
CheckBox_path = tkinter.Checkbutton(text="relative path: check, absolute path: do not check", variable=Val_path)
CheckBox_path.place(x=20, y=20)
Static_path = tkinter.Label(text='directory name of data')
Static_path.pack()
Static_path.place(x=20, y=60)
EditBox_path = tkinter.Entry(width=25)
EditBox_path.insert(tkinter.END,"data")
EditBox_path.place(x=180, y=60)

Static_time = tkinter.Label(text='time interval')
Static_time.pack()
Static_time.place(x=20, y=140)
EditBox_time = tkinter.Entry(width=25)
EditBox_time.insert(tkinter.END,"1")
EditBox_time.place(x=180, y=140)

Static_gas = tkinter.Label(text='Ch (1~4)')
Static_gas.pack()
Static_gas.place(x=20, y=100)

Static_N = tkinter.Label(text='N of points N>=1')
Static_N.pack()
Static_N.place(x=20, y=220)
EditBox_N = tkinter.Entry(width=6)
EditBox_N.insert(tkinter.END,"1")
EditBox_N.place(x=120, y=220)

Static_decay = tkinter.Label(text='decay rate for EWMA')
Static_decay.pack()
Static_decay.place(x=190, y=220)
EditBox_decay = tkinter.Entry(width=6)
EditBox_decay.insert(tkinter.END,"0.1")
EditBox_decay.place(x=320, y=220)

EditBox_gas = tkinter.Entry(width=25)
EditBox_gas.insert(tkinter.END,"1")
EditBox_gas.place(x=180, y=100)

Val_ma = tkinter.BooleanVar()
Val_ma.set(True)
CheckBox_ma = tkinter.Checkbutton(text="moving average    simple: check, exponential: do not check", variable=Val_ma)
CheckBox_ma.place(x=20, y=180)

Button_plot = tkinter.Button(text='plot', width=25)
Button_plot.bind("<Button-1>",ButtonEvent)
Button_plot.place(x=40, y=260)

Button_exit = tkinter.Button(text='exit',command=root.quit, width=10)
Button_exit.place(x=280, y=260)

Val_wireframe = tkinter.BooleanVar()
Val_wireframe.set(False)
CheckBox_wireframe = tkinter.Checkbutton(text=": wireframe", variable=Val_wireframe)
CheckBox_wireframe.place(x=150, y=300)

Val_z = tkinter.BooleanVar()
Val_z.set(False)
CheckBox_z = tkinter.Checkbutton(text=": z manual", variable=Val_z)
CheckBox_z.place(x=150, y=340)

EditBox_zmax = tkinter.Entry(width=15)
EditBox_zmax.insert(tkinter.END,"zmax")
EditBox_zmax.place(x=150, y=380)

EditBox_zmin = tkinter.Entry(width=15)
EditBox_zmin.insert(tkinter.END,"zmin")
EditBox_zmin.place(x=150, y=420)

root.mainloop()
