"""Modeling X-Ray Attenuation through the upper atmosphere
Coded By: Rowan Jansens"""


from tkinter import *
from tkinter.messagebox import showerror
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


#atmospheric data look-up table
atmosphere = [
    [0.000, 1.225000, 288.15, -0.0065],
    [11000, 0.363910, 216.65, 0.00000],
    [20000, 0.088030, 216.65, 0.00100],
    [32000, 0.013220, 228.65, 0.00280],
    [47000, 0.001430, 270.65, 0.00000],
    [51000, 0.000860, 270.65, -0.0028],
    [71000, 0.000064, 214.65, -0.0020],
    [100000, 0, 1, -1]]

#get atmospheric layer based off of current height
def get_layer(height):
    for l in range (8):
        if (height < atmosphere[l][0]):
            return l - 1
        elif (height >= 100000):
            return 7

#use the current layer and the data look-up table to source values for the barometric formulas
#then compute and return the density for the given height
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


#integrate the density function (above) over the start-end height interval
#this effectilvy tells us "how mutch stuff" is in the way of the photons
def average_density(start_height, end_height):
    area = 0
    step = 20   #making this number smaller will increase acuracy but alos make the execution time much longer
    if(start_height <= 100000):
        for i in np.arange (start_height, end_height + step, step):
            area += ((density(i) + density(i + step)) / 2) * step
        return area
    else:
        #this is the most time consumig part of the program so we save time by
        #assuming that the density is always 0 past 100000m
        return 0

#make an intial photon distribution based on a user-input "decay factor" and the energy of the photon bin
def make_photons(energy, decay_factor):
    p = 100 * (decay_factor ** energy)
    return p

#return the attenuation-coefficent for photons of a given energy
#the equation below comes from a power-law fit of NIST x-ray attenuation data.
def get_attcoe(energy):
    attcoe = (393.265 / ((energy ** 2.89148) + 0.0990357)) + 0.0449311;
    return attcoe

#return the photon transmission percentage based off of the average-density and attenuation coefficents
def percent(start_height, end_height, energy):
    percent = math.exp(-1 * get_attcoe(energy) * average_density(start_height, end_height))
    return percent

#build a surface evolution plot
def surface_evolution():

    #first get user inputs
    start_height = e1.get()
    try:
       start_height = int(start_height)
    #if no integer is enterd, show non-int error 
    except ValueError:
        showerror('Start Height Non-Int Error', 'Please enter an integer')
        
    end_height = e2.get()
    try:
       end_height = int(end_height)
    except ValueError:
        showerror('End Height Non-Int Error', 'Please enter an integer')

    decay_factor = e3.get()
    try:
       decay_factor = float(decay_factor)
    except ValueError:
        showerror('Decay Factor Error', 'Please enter a value less than or equal to 1')

    #make some empty lists and define the interval precision
    interval = 2000
    x = np.array([])
    y = np.array([])
    z = np.array([])
    #then append these three lists with the corresponding value as we iterate through the heights and energies
    for h in range (start_height, end_height + interval, interval):
        for e in range (1, 126, 5):
            x = np.append(x, h/1000)    #height in km
            y = np.append(y, e)         #energy in keV
            z = np.append(z, make_photons(e, decay_factor) * percent(start_height, h, e))     #intesnsity

    #plot the data
    fig = plt.figure()
    ax = Axes3D(fig)
    surf = ax.plot_trisurf(x, y, z, cmap=cm.gist_earth, linewidth=0)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_xlabel("Altitude (km)")
    ax.set_ylabel("Photon Energy (keV)")
    ax.set_zlabel("Photon Intensity")
    plt.title("X-Ray Attenuation Through the Upper Atmosphere")
    plt.show()


#build an attenuation line plot
def before_after():
    start_height = e1.get()
    try:
       start_height = int(start_height)
    except ValueError:
        showerror('Start Height Non-Int Error', 'Please enter an integer')

    end_height = e2.get()
    try:
       end_height = int(end_height)
    except ValueError:
        showerror('End Height Non-Int Error', 'Please enter an integer')

    decay_factor = e3.get()
    try:
       decay_factor = float(decay_factor)
    except ValueError:
        showerror('Decay Factor Error', 'Please enter a number less than  or equal to 1')
    
    energy = []
    before = []
    after = []
    for e in range(1,126,5):
        energy.append(e)
        before.append(make_photons(e, decay_factor))
        after.append(make_photons(e, decay_factor) * percent(start_height, end_height, e))
        
    line1, = plt.plot(energy, before)
    line2,  = plt.plot(energy, after)
    plt.legend((line1, line2), ('Initial', 'Final'))
    plt.xlabel("Photon Energy (keV)")
    plt.ylabel("Photon Intensity")
    plt.title("X-Ray Attenuation Through the Upper Atmosphere")
    plt.show()


#build an attenuation line plot using user graph is inital
def forwards():
    start_height = e1.get()
    try:
       start_height = int(start_height)
    except ValueError:
        showerror('Non-Int Error', 'Please enter an integer for the Detonation Altitude')

    end_height = e2.get()
    try:
       end_height = int(end_height)
    except ValueError:
        showerror('Non-Int Error', 'Please enter an integer for the Sensor Altitude')

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


#build an attenuation line plot using user data as final
#In other words: Backtrack based on the rulles of attenuation to see what
#a ditibutin mesured at the sensors would look like at the source.
def backward():
    start_height = e1.get()
    try:
       start_height = int(start_height)
    except ValueError:
        showerror('Non-Int Error', 'Please enter an integer for the Detonation Altitude')

    end_height = e2.get()
    try:
       end_height = int(end_height)
    except ValueError:
        showerror('Non-Int Error', 'Please enter an integer for the Sensor Altitude')
        
    energy = []
    now = []
    then = []
    for i in range(125):
        energy.append(user_graph[i][0])
        now.append(user_graph[i][1])

        #if the tranmition percentage is 0, then we get a devide by zero error
        #instead, we specify a few scenerios in which the value is undefined
        if (percent(start_height, end_height, i+1) < 0.000001):
            then.append(None)
        elif (user_graph[i][1] / percent(start_height, end_height, i+1) > 500):
            then.append(None)

        #if possible, we work backwad by deviding the intesnsity by the the percent instad of
        #multipliy as we did in the other simulations
        else:
            then.append(user_graph[i][1] / percent(start_height, end_height, i+1))

    line3, = plt.plot(energy, now)
    line4,  = plt.plot(energy, then)
    plt.legend((line4, line3), ('Initial', 'Final'))
    plt.xlabel("Photon Energy (keV)")
    plt.ylabel("Photon Intensity")
    plt.title("X-Ray Attenuation Through the Upper Atmosphere")
    plt.show()

def percent_graph():
    start_height = e1.get()
    try:
       start_height = int(start_height)
    except ValueError:
        showerror('Non-Int Error', 'Please enter an integer for the Detonation Altitude')

    end_height = e2.get()
    try:
       end_height = int(end_height)
    except ValueError:
        showerror('Non-Int Error', 'Please enter an integer for the Sensor Altitude')
        
    energy = []
    percentage = []
    for i in range(1,126,1):
        energy.append(i)
        percentage.append(percent(start_height, end_height, i))

    line5, = plt.plot(energy, percentage)
    plt.legend((line5,), ("Percent"))
    plt.xlabel("Photon Energy (keV)")
    plt.ylabel("Transmission Percentage")
    plt.title("X-Ray Attenuation Through the Upper Atmosphere: Trasmission Percent")
    plt.show()

#make a canvas
canvas_width = 4*125
canvas_height = 4*100

#make an empty matrix with rows from 1-125 (energy) and values of 0 (intensity)
user_graph = []
for i in range(1,126,1):
    user_graph.append([i, 0])
    
#Returns a list of coordinate pairs
#Note: all the "*/4s" give the apperance of a more pixelated graph.  
def get_user_graph( event ):

    x = int(event.x/4)   #get x possition of mouse
    #if the mouse is outside of the canvas, constrain the value
    if (x > 125):
        x = 125
    if (x < 1):
        x = 1
        
    y = int(event.y/4)   #get y possition of mouse
    if (y > 100):
        y = 100
    if (y < 0):
        y = 0
        
    c.create_rectangle(4*x, 4*y, 4*x+4, 4*y+4, fill = '#000000' )   #draw a square

    #if the y value is larger than the exsiting value in the matrix, update the matrix with the new value
    #we must also subtract the y value from 100 (the height of the canvas) to get the familiar cartesian coordinates
    if (user_graph[x-1][1] < 100-y):   
        user_graph[x-1][1] = 100-y
        
#add some axis values to the canvas
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

#clear the canvas and reset the user-graph matrix, then draw axis values
def clear_canvas():
    user_graph.clear()
    for i in range(1,126,1):
        user_graph.append([i, 0])
    c.delete("all")
    make_canvas_axis()


root = Tk()
root.title('X-Ray Attenuation')

#Title
l0 = Label(root, font=",18", text="X-Ray Atteunation Through the Upper Atmosphere\n")
l0.pack()

#Detonatiol Altitude Entry Widget + label
e1 = Entry(root, width=30, borderwidth=3)
e1.insert(0, "50000")
l1 = Label(root, text="Enter Detonation Altitude (meters)")
l1.pack()
e1.pack()

#Sensor Altitude Entry Widget + label
e2 = Entry(root, width=30, borderwidth=3)
e2.insert(0, "100000")
l2 = Label(root, text="Enter Sensor Altitude\n(anything above 100km is redundant)")
l2.pack()
e2.pack()

#Percent plot button
button0 = Button(root, text="Line Plot of Trasmission Percentage", width=30, padx=2, pady=5, command=percent_graph)
button0.pack()

#Decay Factor Entry Widget + label
e3 = Entry(root, width=30, borderwidth=3)
e3.insert(0, "0.99")
l3 = Label(root, text="Enter Exponential Decay Factor\n(this determines the shape of the initial photon distribution)")
l3.pack()
e3.pack()

#Line plot button
button1 = Button(root, text="Line Plot of X-Ray Attenuation", width=30, padx=2, pady=5, command=before_after)
button1.pack()

#Surface plot button
button2 = Button(root, text="Surface Plot of X-Ray Attenuation", width=30, padx=2, pady=5, command=surface_evolution)
button2.pack()

l4 = Label(text="\nUse the canvas below to draw a custom graph\nand see how the distribution will change with attenuation.\nYou may use the graph as either the initial or\nfinal distribution in the simulation.\n The x-axis is photon energy in keV and the y-axis is photon intensity")
l4.pack()

#add canvas
c = Canvas(root, width=canvas_width, height=canvas_height, bg='white', bd=3, highlightthickness=3, relief='ridge')
c.pack(expand = FALSE, fill = NONE)
make_canvas_axis()
c.bind( "<B1-Motion>", get_user_graph )


#Clear graph button
button3 = Button(root, text="Clear Graph", command=clear_canvas)
button3.pack()

#Plot as inital button
button4 = Button(root, text="Use Graph as Initial Distribution", width=30, padx=2, pady=5, command=forwards)
button4.pack()

#Plot as final button
button5 = Button(root, text="Use Graph as Final Distribution", width=30, padx=2, pady=5, command=backward)
button5.pack()

root.mainloop()
