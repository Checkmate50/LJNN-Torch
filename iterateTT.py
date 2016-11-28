from __future__ import print_function
from subprocess import call
import sys

def iterate(model, trainFolder, testFolder, iterations, outFile = None, epochs = '1'):
    iterations = int(iterations)
    if iterations <= 0 or int(epochs) <= 0:
        print ("Cannot have iterations or epochs/iteration be nonpositive")
    if not outFile is None:
        lossFile = open(outFile + ".loss", 'w')
        diffFile = open(outFile + ".pdiffs", 'w')
        
    for i in range(iterations):
        call(["th", "trainNN.lua", model, trainFolder, "-e", epochs, "-trr", "deleteMe.txt", "-v", "-pf", "1", "-lr", ".000001"])
        ifile = open("deleteMe.txt")
        for j in ifile:
            if j.strip() == "":
                continue
            print(j, end="")
            if not outFile is None:
                lossFile.write(str(i+1) + "\t" + j.split()[-1] + "\n")
        call(["th", "testNN.lua", model, testFolder, "-ter", "deleteMe.txt"])
        ifile = open("deleteMe.txt")
        for j in ifile:
            if j.strip() == "":
                continue
            print(j, end="")
            if not outFile is None:
                diffFile.write(str(i+1) + "\t" + j.split()[-1][:-1] + "\n")

    call(["rm", "deleteMe.txt"])
    if not outFile is None:
        lossFile.close()
        diffFile.close()

def main() :
    if len(sys.argv) < 5:
        print("Give model name, training folder, test folder, and iteration count in order")
        exit()
    if (len(sys.argv) < 6):
        print("Not writing results to file (no file given)")
    if (len(sys.argv) < 7):
        print("Using default epoch count of 1")
    iterate(*sys.argv[1:])
    
if __name__=="__main__":
    main()
