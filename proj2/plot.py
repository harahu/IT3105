#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def plot(x, y, outfile):
    
    fig = plt.plot(x, y, 'k-')
    #plt.show()
    plt.savefig(outfile, format='png', pad_inches=0.0)
    plt.clf()

