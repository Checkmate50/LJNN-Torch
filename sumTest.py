import sys
import random
from inspect import getargspec

def simple_mult(x, y, z):
    return x*y*z + z

def writeBatch(filename, rows, fun):
    f = open(filename, 'w')
    sum = 0
    for i in range(rows):
        args = [random.random() for i in getargspec(fun)[0]]
        for i in args[:-1]:
            f.write(str(i)+ " ")
        f.write(str(args[-1])+ "\n")
        sum += fun(*args)
    f.write(str(sum))
    f.close()

def main():
    if len(sys.argv) < 3:
        print("Not enough arguments")
        return
    fileCount = int(sys.argv[1])
    folder = str(sys.argv[2])
    rows = 512
    if len(sys.argv) > 3:
        rows = int(sys.argv[3])

    for i in range(1, fileCount+1):
        nextFile = folder + str(i) + ".nndata"
        print("Writing " + nextFile)
        writeBatch(nextFile, rows, simple_mult)

if __name__=="__main__":
    main()
