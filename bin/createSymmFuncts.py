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

def getFc(i):
    if i == 1:
        return f1
    return f2

def g2(f, Rc, eta, Rs, i, atomList, box):
    fc = getFc(f)
    sum = 0
    for j in atomList:
        if i == j:
            continue
        Rij = i.calcDist(j, box)
        sum += math.exp(-eta*(Rij-Rs)**2)*fc(Rc, Rij)
    return sum

def get2Functs(functions, Rc, sigma, count):
    to_return = []
    if not isinstance(functions, list):
        functions = [functions]
        Rc = [Rc]
        sigma = [sigma]
        count = [count]
    for i in range(len(functions)):
        eta = 1/(2*sigma[i])
        for offset in range(count[i]):
            Rs = offset*(Rc[i]-sigma[i])/count[i] + sigma[i]
            to_return.append(partial(g2, f = functions[i], Rc = Rc[i], eta = eta, Rs = Rs))
    return to_return


def get3Functs(functions, Rc, sigma, count):
    # UPDATE!!!!
    to_return = []
    if not isinstance(functions, list):
        functions = [functions]
        Rc = [Rc]
        sigma = [sigma]
        count = [count]
    for i in range(len(functions)):
        eta = 1/(2*sigma[i])
        for offset in range(count[i]):
            Rs = offset*(Rc[i]-sigma[i])/count[i] + sigma[i]
            to_return.append(partial(g2, f = functions[i], Rc = Rc[i], eta = eta[i], Rs = Rs[i]))
    return to_return
