import tkinter
from global_data import *


def create_circle(x, y, r, canvas,f="blue"): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1,fill=f)

def create_square(x, y, r, canvas): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_rectangle(x0, y0, x1, y1, fill='red', outline='black')

colors = ["blue","red","green","black","cyan","magenta","pink","violet","yellow","grey","gold","brown","beige","silver","AliceBlue", "AntiqueWhite", "AntiqueWhite1", "AntiqueWhite2", "AntiqueWhite3",    "AntiqueWhite4", "aquamarine", "aquamarine1", "aquamarine2", "aquamarine3",    "aquamarine4", "azure", "azure1", "azure2", "azure3", "azure4", "beige",    "bisque", "bisque1", "bisque2", "bisque3", "bisque4", "black", "BlanchedAlmond",    "blue", "blue1", "blue2", "blue3", "blue4", "BlueViolet", "brown", "brown1",    "brown2", "brown3", "brown4", "burlywood", "burlywood1", "burlywood2", "burlywood3",    "burlywood4", "CadetBlue", "CadetBlue1", "CadetBlue2", "CadetBlue3", "CadetBlue4",    "chartreuse", "chartreuse1", "chartreuse2", "chartreuse3", "chartreuse4"]

def display_routes(R):
    global colors,points
    N=len(points)
    x=[float(points[i][0]) for i in range(N)]
    y=[float(points[i][1]) for i in range(N)]
    mx=min(x)
    Mx=max(x)
    my=min(y)
    My=max(y)
    height=720
    width=1280
    Ep=[[(x[i]-mx)*width/(Mx-mx),(y[i]-my)*height/(My-my),i] for i in range(N)]
    top = tkinter.Tk()
    C = tkinter.Canvas(top, bg="white", height=height, width=width)
    for r in range(len(R)):
        
        for e in R[r]:
            create_circle(int(Ep[e][0]),int(Ep[e][1]),4,C,colors[r])
        for i in range(len(R[r])-1):
            C.create_line(Ep[R[r][i]][0],Ep[R[r][i]][1],Ep[R[r][i+1]][0],Ep[R[r][i+1]][1], fill=colors[r], width=1)
        
        
    C.pack()
    top.mainloop()


def display_routes(R):
    global colors, points
    N = len(points)
    x = [float(points[i][0]) for i in range(N)]
    y = [float(points[i][1]) for i in range(N)]
    mx = min(x)
    Mx = max(x)
    my = min(y)
    My = max(y)
    height = 720
    width = 1280
    Ep = [[(x[i] - mx) * width / (Mx - mx), (y[i] - my) * height / (My - my), i] for i in range(N)]
    top = tkinter.Tk()
    C = tkinter.Canvas(top, bg="white", height=height, width=width)
    for r in range(len(R)):

        for e in R[r]:
            create_circle(int(Ep[e][0]), int(Ep[e][1]), 4, C, colors[r])
        for i in range(len(R[r]) - 1):
            C.create_line(Ep[R[r][i]][0], Ep[R[r][i]][1], Ep[R[r][i + 1]][0], Ep[R[r][i + 1]][1], fill=colors[r],
                          width=1)

    C.pack()
    top.mainloop()

def display_facilities(opened_facilities,serving_matrix,locations):
    global colors, points
    N = len(points)
    x = [float(points[i][0]) for i in range(N)]
    y = [float(points[i][1]) for i in range(N)]
    mx = min(x)
    Mx = max(x)
    my = min(y)
    My = max(y)
    height = 720
    width = 1280
    Ep = [[(x[i] - mx) * width / (Mx - mx), (y[i] - my) * height / (My - my), i] for i in range(N)]
    top = tkinter.Tk()
    C = tkinter.Canvas(top, bg="white", height=height, width=width)

    for j in locations:
        if opened_facilities[j]==1:
            create_square(int(Ep[j][0]), int(Ep[j][1]), 4, C)
        else:
            create_circle(int(Ep[j][0]), int(Ep[j][1]), 4, C)

    for i in locations:
        for j in locations:
            if serving_matrix[i][j]==1:
                C.create_line(Ep[i][0], Ep[i][1], Ep[j][0], Ep[j][1], fill='black', width=1)
    C.pack()
    top.mainloop()
