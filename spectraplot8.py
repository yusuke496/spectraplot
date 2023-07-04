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

def ButtonEvent(event):
    dirofdata = EditBox3.get()
    if Val1.get() == False:
        path = os.path.dirname(os.path.abspath(__file__))+"\\"+dirofdata
    else:
        path = EditBox3.get()
    #print(path)
    list = os.listdir(path)
    #複数の数字を含む文字列のソート
    list0=sorted(list, key=lambda s: int(re.search(r'(\d+)min', s).groups()[0]))
    #sorted(list, key=lambda s: int(re.findall(r'\d+', s)[1]))
    #print(list0)
    noffile = len(list0)
    tstepc = EditBox1.get()
    tstep = int(tstepc)
    Chc = EditBox2.get()
    Ch = int(Chc)
    mac = EditBox4.get()
    ma = int(mac)
#    print(Val2.get())
#    if Val2.get() == True:
#        xlim1c=EditBox5.get()
#        xlim2c=EditBox4.get()
#        xlim1=float(xlim1c)
#        xlim2=float(xlim2c)
#    else:
#        pass
#
#    if Val3.get() == True:
#        ylim1c = EditBox7.get()
#        ylim1 = float(ylim1c)
#        ylim2c = EditBox6.get()
#        ylim2 = float(ylim2c)
#    else:
#        pass

    if Val4.get() == True:
        zlim1c = EditBox9.get()
        zlim1 = float(zlim1c)
        zlim2c = EditBox8.get()
        zlim2 = float(zlim2c)
    else:
        pass

    ylist = [ i*tstep for i in range(noffile) ]
    xlist = [ i for i in range(250) ]
    #print(xlist,ylist)
    data=[]
    ColNum = 3*Ch+2
    for filename in list0:
        filepath = path+"\\"+filename
        #print(filepath)
        csvdata = pd.read_csv(filepath, header=None)
        databf=np.array(csvdata.values[0:250,ColNum])
        #print(databf)
        databf=databf-mean(databf)
        databf=moav(databf,ma)
        data.append(databf)
    #print(len(data[0]))

    X, Y = np.meshgrid(np.array(xlist), np.array(ylist))
    Z = np.array(data)
    fig = plt.figure(figsize=(6,4))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel("points")
    ax.set_ylabel("time (min)")
    ax.set_zlabel("abs")

#    if Val2.get() == True:
#        ax.set_xlim3d(xlim1,xlim2)
#    else:
#        pass
#    if Val3.get() == True:
#        ax.set_ylim3d(ylim1,ylim2)
#    else:
#        pass
    if Val4.get() == True:
        ax.set_zlim3d(zlim1,zlim2)
    else:
        pass

    if Val5.get() == False:
        surf = ax.plot_surface(X, Y, Z, cmap='plasma', linewidth=1)
        fig.colorbar(surf)
        fig.show()
    else:
        ax.plot_wireframe(X, Y, Z, color='blue',linewidth=0.2)
        fig.show()

root = tkinter.Tk()
root.title("Spectra Plot")
root.geometry("400x400")

#チェックボックスの各項目の初期値
Val1 = tkinter.BooleanVar()
Val1.set(False)
CheckBox1 = tkinter.Checkbutton(text="full path: check, relative path: do not check", variable=Val1)
CheckBox1.place(x=20, y=20)

#var1 = tkinter.IntVar()
#var1.set(0)

#var2 = tkinter.IntVar()
#var2.set(0)

#ラジオボタン
#rdo1 = tkinter.Radiobutton(root, value=0, variable=var1, text='Pressure')
#rdo1.place(x=100, y=30)

#rdo2 = tkinter.Radiobutton(root, value=1, variable=var1, text='Temparature')
#rdo2.place(x=100, y=50)

#rdo3 = tkinter.Radiobutton(root, value=0, variable=var2, text='Long path')
#rdo3.place(x=250, y=30)

#rdo4 = tkinter.Radiobutton(root, value=1, variable=var2, text='Short path')
#rdo4.place(x=250, y=50)

Static1 = tkinter.Label(text='time step')
Static1.pack()
Static1.place(x=20, y=60)

Static2 = tkinter.Label(text='Ch (0~3)')
Static2.pack()
Static2.place(x=20, y=90)

Static3 = tkinter.Label(text='directory name of data')
Static3.pack()
Static3.place(x=20, y=120)

Static10 = tkinter.Label(text='moveing average N>=1')
Static10.pack()
Static10.place(x=20, y=150)

#Static4 = tkinter.Label(text='Temp (-0.1~0.1)')
#Static4.pack()
#Static4.place(x=20, y=130)

#Static5 = tkinter.Label(text='Press (18~44)')
#Static5.pack()
#Static5.place(x=20, y=150)

#Static6 = tkinter.Label(text='Press(0) or Temp(1)')
#Static6.pack()
#Static6.place(x=30, y=20)

#Static7 = tkinter.Label(text='LP(0)/SP(1)')
#Static7.pack()
#Static7.place(x=30, y=40)

EditBox1 = tkinter.Entry(width=25)
EditBox1.insert(tkinter.END,"1")
EditBox1.place(x=180, y=60)

EditBox2 = tkinter.Entry(width=25)
EditBox2.insert(tkinter.END,"0")
EditBox2.place(x=180, y=90)

EditBox3 = tkinter.Entry(width=25)
EditBox3.insert(tkinter.END,"data")
EditBox3.place(x=180, y=120)

EditBox4 = tkinter.Entry(width=25)
EditBox4.insert(tkinter.END,"1")
EditBox4.place(x=180, y=150)

Button1 = tkinter.Button(text='plot', width=15)
Button1.bind("<Button-1>",ButtonEvent)#左クリック（<Button-1>）されると，ButtonEvent関数を呼び出すようにバインド
Button1.place(x=40, y=180)

Button2 = tkinter.Button(text='exit',command=root.quit, width=15)
Button2.place(x=250, y=180)

#Val2 = tkinter.BooleanVar()
#Val2.set(False)
#CheckBox2 = tkinter.Checkbutton(text="x manual:", variable=Val2)
#CheckBox2.place(x=20, y=250)

#EditBox4 = tkinter.Entry(width=15)
#EditBox4.insert(tkinter.END,"xmax")
#EditBox4.place(x=20, y=300)

#EditBox5 = tkinter.Entry(width=15)
#EditBox5.insert(tkinter.END,"xmin")
#EditBox5.place(x=20, y=350)

#Val3 = tkinter.BooleanVar()
#Val3.set(False)
#CheckBox2 = tkinter.Checkbutton(text="y manual:", variable=Val3)
#CheckBox2.place(x=150, y=250)

#EditBox6 = tkinter.Entry(width=15)
#EditBox6.insert(tkinter.END,"ymax")
#EditBox6.place(x=150, y=300)

#EditBox7 = tkinter.Entry(width=15)
#EditBox7.insert(tkinter.END,"ymin")
#EditBox7.place(x=150, y=350)

Val4 = tkinter.BooleanVar()
Val4.set(False)
CheckBox2 = tkinter.Checkbutton(text=": z manual", variable=Val4)
CheckBox2.place(x=150, y=250)

Val5 = tkinter.BooleanVar()
Val5.set(False)
CheckBox3 = tkinter.Checkbutton(text=": wireframe", variable=Val5)
CheckBox3.place(x=150, y=220)

EditBox8 = tkinter.Entry(width=15)
EditBox8.insert(tkinter.END,"zmax")
EditBox8.place(x=150, y=300)

EditBox9 = tkinter.Entry(width=15)
EditBox9.insert(tkinter.END,"zmin")
EditBox9.place(x=150, y=350)

Val5 = tkinter.BooleanVar()
Val5.set(False)
CheckBox3 = tkinter.Checkbutton(text=": wireframe", variable=Val5)
CheckBox3.place(x=150, y=220)

root.mainloop()
