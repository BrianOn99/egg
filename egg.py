#!/usr/bin/python
# coding: utf-8
import matplotlib.pyplot as plt
from matplotlib import animation
from math import *

cir1 = {"cen":(0,0), "r":3.5}
cir2 = {"cen":(2.8,0), "r":5}

fig = plt.figure(figsize=(10,7))
axes = fig.add_subplot(111, axisbg="#444444")
axes.set_xlim([-10,10])
axes.set_ylim([-7,7])
axes.xaxis.set_visible(False)
axes.yaxis.set_visible(False)
cir1["tome"], = axes.plot([], [], lw=2, color="#77bbff")
cir1["toyou"], = axes.plot([], [], lw=2, color="#f5ccff")
cir2["tome"], = axes.plot([], [], lw=2, color="#77bbff")
cir2["toyou"], = axes.plot([], [], lw=2, color="#f5ccff")
eggpt = ([], [])
egg, = axes.plot(*eggpt, color="#ffe29e", lw=4)

circle1=plt.Circle(cir1["cen"], cir1["r"], color='#bbbbbb', lw=2, fill=False)
circle2=plt.Circle(cir2["cen"], cir2["r"], color='#ffffff', lw=2, fill=False)
axes.add_artist(circle1)
axes.add_artist(circle2)
plt.ion()

def cir_radial(x, r, theta):
    return sqrt(r**2 - (x*sin(theta))**2) + x*cos(theta)

class ZeroLenError(ArithmeticError):
    pass

def slope(p1, p2):
    try:
        sl = (p2[1]-p1[1]) / (p2[0]-p1[0])
    except ZeroDivisionError as exc:
        if (p2[1]-p1[1]) == 0:
            raise ZeroLenError from exc
        sl = float("inf")
    return sl

def interection(pa1, pa2, pb1, pb2):
    # y = mx + C
    ma = slope(pa1, pa2)
    mb = slope(pb1, pb2)
    Ca = -ma*pa2[0] + pa2[1]
    Cb = -mb*pb2[0] + pb2[1]
    x = (Ca-Cb) / (mb-ma)
    y = ma*x + Ca
    return (x, y)

def init():
    cir1["tome"].set_data([], [])
    cir1["toyou"].set_data([], [])
    cir2["tome"].set_data([], [])
    cir2["toyou"].set_data([], [])
    egg.set_data([], [])
    return (cir1["tome"], cir2["tome"], cir1["toyou"], cir2["toyou"], egg)

def draw(theta):
    if theta % pi == 0: return
    len1to2= cir_radial(cir2["cen"][0], cir2["r"], theta)
    len2to1= cir_radial(-cir2["cen"][0], cir1["r"], theta)
    touch_pt2 = len1to2*cos(theta), len1to2*sin(theta)
    touch_pt1 = cir2["cen"][0]+len2to1*cos(theta), cir2["cen"][1]+len2to1*sin(theta)
    cross_pt = interection(cir1["cen"], touch_pt1, cir2["cen"], touch_pt2)
    eggpt[0].append(cross_pt[0]), eggpt[1].append(cross_pt[1]), 
    egg.set_data(*eggpt)

    for host, ptme, ptyou in ((cir1, touch_pt1, touch_pt2),
                              (cir2, touch_pt2, touch_pt1)):
        cen = host["cen"]
        host["tome"].set_data((cen[0], ptme[0]), (cen[1], ptme[1]))
        host["toyou"].set_data((cen[0], ptyou[0]), (cen[1], ptyou[1]))

deltaangle = 0.05
def animate(i):
    draw(i*deltaangle)
    return (cir1["tome"], cir2["tome"], cir1["toyou"], cir2["toyou"], egg)

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=int(4*pi/deltaangle), interval=40, blit=True)

anim.save('drawegg.mp4', fps=40,  extra_args=['-vcodec', 'libx264'])
