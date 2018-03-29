#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import event
import sys, os, h5py

e1 = event.event(M=1.3)

# https://arxiv.org/pdf/1205.2396.pdf
initial = {'c': lambda x: x/(x**2+2.1**2)**3.9,
		   'b': lambda x: x/(x**2+7.5**2)**4.9 }

e1.initialize_HQ(200000, {"type":"box", "pmax": 120., "L":1})

p0, x0 = e1.HQ_hist()
T0 = 0.4
tstart = 0.0
for i in range(80):
	if i%10 ==0:
		print(i, "steps")
	e1.perform_hydro_step({"Temp":T0, "Vx":0.0, "Vy":0.0, "Vz":0.})

p1, x1 = e1.HQ_hist()

pT0 = np.sqrt(np.sum(p0.T[1:]**2, axis=0))
pT1 = np.sqrt(np.sum(p1.T[1:]**2, axis=0))

w = initial['c'](pT0)

H0, x0 = np.histogram(pT0, 50, weights=w, normed=True, range=[0,100])
H1, x0 = np.histogram(pT1, 50, weights=w, normed=True, range=[0,100])
x0 = (x0[1:]+x0[:-1])/2.
plt.plot(x0, H1/H0, 'r-')
plt.ylim(0,1.5)
plt.show()

with open("BoxRaa-mu1-charm.dat",'w') as f:
	for ix, iR in zip(x0, H1/H0):
		print(ix, iR, file=f)


