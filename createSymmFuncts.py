from functools import partial
from math import pi
import math

def foo(x, y):
    return x + y

def foo2(x):
    return partial(foo, x)

def f1(Rc, Rij):
    if Rij > Rc:
        return 0
    return .5*(math.cos(pi*Rij/Rc)+1)

def f2(Rc, Rij):
    if Rij > Rc:
        return 0
    return math.tanh(1-(Rij/Rc))**3

def getFc(i, Rc):
    #Returns f_i with a constant cutoff of Rc
    if i == 1:
        return partial(f1, Rc)
    return partial(f2, Rc)

def g2(f, Rc, nu, Rs, i, atomList):
    #atomList must be a list with all Atoms besides "i"
    fc = getFc(f, Rc)
    sum = 0
    for j in atomList:
        Rij = i.calcDist(j)
        sum += math.exp(-nu*(Rij-Rs)**2)*fc(Rij)
    return sum

def getFuncts(Rc, sigma, count):
    nu = 1/(2*sigma)
    toReturn = []
    for offset in range(count):
        Rs = offset*(Rc-sigma)/count + sigma
        toReturn.append(partial(g2, 1, Rc, nu, Rs))
    return toReturn
