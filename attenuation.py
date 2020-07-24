from tkinter import *
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import csv
import time
from mpl_toolkits.mplot3d import Axes3D
from tkinter.messagebox import showerror



atmosphere = [
    [0.000, 1.225000, 288.15, -0.0065],
    [11000, 0.363910, 216.65, 0.00000],
    [20000, 0.088030, 216.65, 0.00100],
    [32000, 0.013220, 228.65, 0.00280],
    [47000, 0.001430, 270.65, 0.00000],
    [51000, 0.000860, 270.65, -0.0028],
    [71000, 0.000064, 214.65, -0.0020],
    [100000, 0, 1, -1]]

def get_layer(height):
    for l in range (8):
        if (height < atmosphere[l][0]):
            return l - 1
        elif (height >= 100000):
            return 7

def density(height):
    layer = get_layer(height)
    l_height = atmosphere[layer][0]
    l_den = atmosphere[layer][1]
    l_temp = atmosphere[layer][2]
    l_lapse = atmosphere[layer][3]

    if (layer == 7):
        return 0
    elif (l_lapse != 0):
        base = l_temp / (l_temp + l_lapse * (height - l_height))
        exponent = 1 + ((9.80665 * 0.0289644) / (8.3144598 * l_lapse))
        density = l_den * (base ** exponent);
        return density;
    else:
        exponent = (-9.80665 * 0.0289644 * (height - l_height)) / (8.3144598 * l_temp);
        density = l_den * math.exp(exponent);
        return density;
    
def average_density(start_height, end_height):
    area = 0
    step = 10
    if(start_height <= 100000):
        for i in np.arange (start_height, end_height + step, step):
            area += ((density(i) + density(i + step)) / 2) * step
        return area
    else:
        return 0

def make_photons(energy):
    p = 100 * (0.99 ** energy)
    return p

def get_attcoe(energy):
    attcoe = (393.265 / ((energy ** 2.89148) + 0.0990357)) + 0.0449311;
    return attcoe

def percent(start_height, end_height, energy):
    percent = math.exp(-1 * get_attcoe(energy) * average_density(start_height, end_height))
    return percent

def surface_evolution():
    start_height = e1.get()
    try:
       start_height = int(start_height)
    except ValueError:
        showerror('Non-Int Error', 'Please enter an integer')

    end_height = e2.get()
    try:
       end_height = int(end_height)
    except ValueError:
        showerror('Non-Int Error', 'Please enter an integer')

    interval = 2000
    x = np.array([])
    y = np.array([])
    z = np.array([])
    for h in range (start_height, end_height + interval, interval):
        for e in range (1, 126, 5):
            x = np.append(x, h/1000)
            y = np.append(y, e)
            z = np.append(z, make_photons(e) * percent(start_height, h, e))

    fig = plt.figure()
    ax = Axes3D(fig)
    surf = ax.plot_trisurf(x, y, z, cmap=cm.gray, linewidth=0)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

def before_after():
    start_height = e1.get()
    try:
       start_height = int(start_height)
    except ValueError:
        showerror('Non-Int Error', 'Please enter an integer')

    end_height = e2.get()
    try:
       end_height = int(end_height)
    except ValueError:
        showerror('Non-Int Error', 'Please enter an integer')
    
    energy = []
    before = []
    after = []
    for e in range(1,126,5):
        energy.append(e)
        before.append(make_photons(e))
        after.append(make_photons(e) * percent(start_height, end_height, e))
        
    line1, = plt.plot(energy, before)
    line2,  = plt.plot(energy, after)
    plt.legend((line1, line2), ('Before', 'After'))
    plt.xlabel("Photon Energy (keV)")
    plt.ylabel("Photon Intensity")
    plt.title("X-Ray Attenuation Through the Upper Atmosphere")
    plt.show()

def forwards():
    start_height = e1.get()
    try:
       start_height = int(start_height)
    except ValueError:
        showerror('Non-Int Error', 'Please enter an integer')

    end_height = e2.get()
    try:
       end_height = int(end_height)
    except ValueError:
        showerror('Non-Int Error', 'Please enter an integer')
    energy = []
    now = []
    then = []
    for i in range(125):
        energy.append(user_graph[i][0])
        now.append(user_graph[i][1])
        then.append(user_graph[i][1] * percent(start_height, end_height, i+1))
    line5, = plt.plot(energy, now)
    line6,  = plt.plot(energy, then)
    plt.legend((line5, line6), ('Initial', 'Final'))
    plt.xlabel("Photon Energy (keV)")
    plt.ylabel("Photon Intensity")
    plt.title("X-Ray Attenuation Through the Upper Atmosphere")
    plt.show()

def backward():
    start_height = e1.get()
    try:
       start_height = int(start_height)
    except ValueError:
        showerror('Non-Int Error', 'Please enter an integer')

    end_height = e2.get()
    try:
       end_height = int(end_height)
    except ValueError:
        showerror('Non-Int Error', 'Please enter an integer')
    energy = []
    now = []
    then = []
    for i in range(125):
        energy.append(user_graph[i][0])
        now.append(user_graph[i][1])
        if (percent(start_height, end_height, i+1) < 0.000001):
            then.append(None)
        elif (user_graph[i][1] / percent(start_height, end_height, i+1) > 500):
            then.append(None)
        else:
            then.append(user_graph[i][1] / percent(start_height, end_height, i+1))
    line3, = plt.plot(energy, now)
    line4,  = plt.plot(energy, then)
    plt.legend((line4, line3), ('Initial', 'Final'))
    plt.xlabel("Photon Energy (keV)")
    plt.ylabel("Photon Intensity")
    plt.title("X-Ray Attenuation Through the Upper Atmosphere")
    plt.show()

def main():
    for i in range(len(user_graph)):
        print(user_graph[i])

canvas_width = 4*125
canvas_height = 4*100

user_graph = []
for i in range(1,126,1):
    user_graph.append([i, 0])
    

def get_user_graph( event ):
    color = "#000000"
    x = int(event.x/4)
    if (x > 125):
        x = 125
    if (x < 1):
        x = 1
    y = int(event.y/4)
    if (y > 100):
        y = 100
        
    c.create_rectangle(4*x, 4*y, 4*x+4, 4*y+4, fill = color )

    if (user_graph[x-1][1] < 100-y):
        user_graph[x-1][1] = 100-y

def make_canvas_axis():
    c.create_text(9, 400, text="0")
    
    c.create_text(100, 400, text="25")
    c.create_text(200, 400, text="50")
    c.create_text(300, 400, text="75")
    c.create_text(400, 400, text="100")
    c.create_text(494, 400, text="125")

    c.create_text(13, 320, text="20")
    c.create_text(13, 240, text="40")
    c.create_text(13, 160, text="60")
    c.create_text(13, 80, text="80")
    c.create_text(17, 11, text="100")

def clear_canvas():
    user_graph.clear()
    for i in range(1,126,1):
        user_graph.append([i, 0])
    c.delete("all")
    make_canvas_axis()

    




root = Tk()
root.title('X-Ray Attenuation')

e1 = Entry(root, width=20, borderwidth=3)
e1.insert(0, "40000")
e1.pack()
#e1.grid(row=0, column=0, padx=2, pady=5)

e2 = Entry(root, width=20, borderwidth=3)
e2.insert(0, "50000")
e2.pack()
#e2.grid(row=0, column=1, padx=2, pady=5)

button1 = Button(root, text="Default Before-After Graph", width=42, padx=2, pady=5, command=before_after)
button1.pack()
#button1.grid(row=1, column=0, columnspan=2)

button2 = Button(root, text="Surface-Evolution Graph", width=42, padx=2, pady=5, command=surface_evolution)
button2.pack()
#button2.grid(row=2, column=0, columnspan=2)

button4 = Button(root, text="Plot Graph as Inital Distribution", width=42, padx=2, pady=5, command=forwards)
button4.pack()
#button4.grid(row=3, column=0, columnspan=2)

button5 = Button(root, text="Plot Graph as Final Distribution", width=42, padx=2, pady=5, command=backward)
button5.pack()
#button5.grid(row=3, column=0, columnspan=2)



c = Canvas(root, width=canvas_width, height=canvas_height, bg='white', bd=3, highlightthickness=3, relief='ridge')
c.pack(expand = FALSE, fill = NONE)
make_canvas_axis()
c.bind( "<B1-Motion>", get_user_graph )

button3 = Button(root, text="Clear Graph", command=clear_canvas)
button3.pack()



root.mainloop()

"""start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))"""
