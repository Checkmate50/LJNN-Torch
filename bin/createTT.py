#!/usr/local/bin/python
import math
import random
import os
import sys
from createSymmFuncts import SymmFunct2, SymmFunct3
from lammpstrjToData import lammpstrj_to_data
import helper
from subprocess import call
import numpy as np

"""
This script creates the training and testing files for training and neural network from lammps data.  If generateData is True, this script first generates this data before writing the appropriate files.

Input:
lammpstrj and log file names located in ../lammps_data/
Files should be generated via a run of lammps and follow this format
(OPTIONAL)
Give the folder where the train and test files (respectively) should be placed
[default trainFiles/ and testFiles/]
Additionally, give the location where scaling.data and input.nn should be written
[default ../runner/]

Output:
The train/test files generated via running symmetry functions on the given input files
And the scaling and input information for runner
Note that, as usual, this input information relies on the on information given in main.info
So make sure this file is formatted correctly!!

Written by Dietrich Geisler
"""

class Box:
    def __init__(self, basis):
        self.x_y_tilt = basis[1][0]/basis[1][1];
        self.x_z_tilt = (basis[1][0]*basis[2][0]-basis[1][1]*basis[2][0])/(basis[1][1]*basis[2][2]);
        self.y_z_tilt = basis[2][1]/basis[2][2];
        self.basis=basis

class Atom:
    def __init__(self, pos, element, force):
        #Note that the box and atom are translated so that the box originates at (0, 0, 0)
        self.pos = pos
        self.element = element
        self.force = force

    def calcDistOrtho(self, other, box):
        """
        Figures out the closest 'version' of the other atom assuming an orthorhombic
                box (so basically useless!!!)
        Returns the symmetry function result associated with this closest version
        """
        
        self.checkDim(other)
        diffs = [self.pos[i]-other.pos[i] for i in range(len(self.pos))]
        r_vals = []

        #Account for x, y extensions out of box
        r_vals.append(math.sqrt(sum([i**2 for i in diffs])))
        for i in range(len(box)):
            diffs[i] += box[i]  #positive shift
            r_vals.append(math.sqrt(sum([j**2 for j in diffs])))
            diffs[i] -= box[i]*2  #negative shift
            r_vals.append(math.sqrt(sum([j**2 for j in diffs])))
            diffs[i] += box[i]  #return to original

        return min(r_vals), box
        
    def calcDist(self,other,box):
        """
        Calculates and returns the closest version of the other atom given a box (which is potentially tilted)
        """
        self.checkDim(other)
        z=self.pos[2]-other.pos[2]
        y=self.pos[1]-other.pos[1]
        x=self.pos[0]-other.pos[0]
        if(z < -box.basis[2][2]/2.):
            x += box.basis[2][0]
            y += box.basis[2][1]
            z += box.basis[2][2]
        elif(z > box.basis[2][2]/2.):
            x -= box.basis[2][0]
            y -= box.basis[2][1]
            z -= box.basis[2][2]
        if(y + z*box.y_z_tilt < -box.basis[1][1]/2. ):
            x += box.basis[1][0]
            y += box.basis[1][1]
        elif(y + z*box.y_z_tilt > box.basis[1][1]/2. ):
            x -= box.basis[1][0]
            y -= box.basis[1][1]
        if(x + box.x_y_tilt * y + box.x_z_tilt * z < -box.basis[0][0]/2.):
            x += box.basis[0][0]
        elif(x + box.x_y_tilt * y + box.x_z_tilt * z > box.basis[0][0]/2.):
            x -= box.basis[0][0]
        return(math.sqrt(z**2.0+y**2.0+x**2.0))


    def checkDim(self, other):
        #Prints dimension warnings as needed
        if len(self.pos) != len(other.pos):
            helper.print_warning("WARNING: two compared atoms have different position dimensions")
                
    def __str__(self):
        return self.element + " at " + str(self.pos)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Atom):
            return False
        return self.pos == other.pos


def generateData(lammps_file, seed, data_file, runner_folder):
    """
    Given a lammps_file, seed, and a place to write this information to runner
    Generates the data from the lammps file
    """
    lammps_filename = lammps_file[(max(lammps_file.rfind("/"), lammps_file.rfind("\\")) + 1):]
    lammps_dir = lammps_file[:(len(lammps_file)-len(lammps_filename))]
    os.chdir(lammps_dir)
    with open("runCommand.bash", "w") as f:
        f.write("lammps -echo screen -var seed " + str(seed) + " < " + lammps_filename)
    call(["bash", "runCommand.bash"])
    for i in range(max(lammps_dir.count("/"), lammps_dir.count("\\"))):
        os.chdir("..")
    call(["mv", lammps_dir + "runCommand.bash", runner_folder + "runCommand.bash"])
    lammpstrj = ""
    log = lammps_dir + "log.lammps"
    # Copy lammps file to the runner folder
    with open(lammps_file, "r") as fi:
        with open(runner_folder + lammps_filename, "w") as fo:
            for line in fi:
                if line.strip().startswith("pair_style"):
                    fo.write("variable\tout equal 100\t# frequency of writing thermo quantities to output file\n")
                    fo.write("pair_style\trunner showew no showewsum ${out} maxew 10000 resetew yes dir .\n")
                    line = "#" + line
                if line.strip().startswith("pair_coeff"):
                    fo.write("pair_coeff\t* * 6.350126988  #12 angstrum\n")
                    line = "#" + line
                elif line.strip().startswith("dump"):
                    lammpstrj = lammps_dir + line[:line.find(".lammpstrj")].split()[-1] + ".lammpstrj"
                elif line.strip().startswith("log"):
                    log = lammps_dir + line.split()[-1]
                fo.write(line)
    if not lammpstrj:
        helper.print_error("ERROR: lammpstrj file not written using dump, cannot proceed")
        exit()
    print("converting to data!")
    print data_file, log, lammpstrj
    lammpstrj_to_data(data_file, log, lammpstrj)


def getSymmFunctions(symmFunctInfo):
    to_return = []
    with open(symmFunctInfo, "r") as f:
        for line in f:
            sline = list(map(helper.reduce_type, line[:line.find("#")].strip().split()))
            if len(sline) < 2:
                continue
            if sline[0] == 2:
                to_return.append(SymmFunct2(*sline[1:]))
            elif sline[0] == 3:
                to_return.append(SymmFunct3(*sline[1:]))
            else:
                helper.print_warning("WARNING: " + str(sline[0]) + " unrecognized symmetry function type")
    return to_return
    
def readAtomData(filename):
    """
    Reads in the atoms of a .data file and assigns them the symmetry function symmFun
    Returns an array of atoms for each time step (each combined as an array)
    """

    if not filename.endswith("data"):
        helper.print_warning("WARNING: the atom file " + filename + " is not a .data file")
    
    f = open(filename, 'r')
    step_data = []
    energy = 0
    box_data = []
    atomData = []
    thermoData = []

    with open(filename, 'r') as f:
        for line in f:
            sline = line.strip().lower().split()
            if sline[0] == "end":
                atomData.append([getAtoms(step_data), getBox(box_data)])
                thermoData.append(energy)
                box_data = []
                step_data = []
            if sline[0] == "lattice":
                box_data.append(line)
            elif sline[0] == "atom":
                step_data.append(line)
            elif sline[0] == "energy":
                energy = float(sline[1])
                
    return atomData, thermoData

def getBox(box_data):
    """
    Given a nxn lattice of box data (with keywords in the first column)
    Returns the Box object representing this box
    """
    return Box([list(map(float, dim.split()[1:])) for dim in box_data])

def getAtoms(step_data):
    """
    Given a timestep worth of atoms
    Reads and returns the data in that timestep

    Note that we assume individual atom information follows the format:
    atom x y z element_str s_at_e charge fx fy fz
    """
    to_return = []
    line = step_data[0][len("ITEM: ATOMS"):]
    ls = line.strip().split()
    pos_index = 1
    element_index = 4
    force_index = 7
    for line in step_data:
        ls = line.strip().split()
        pos = [float(ls[i+pos_index]) for i in range(3)]
        element = ls[element_index]
        force = [float(ls[i+pos_index]) for i in range(3)]
        to_return.append(Atom(pos, element, force))
    return to_return


def getScalingData(atoms, symmFuncts):
    """
    Given a list of configurations
    - 3-dimensional arrays with atomic positions, a potential energy, and a box -
    Calculates the scaling data for each configuration of atoms
    And computes the metadata for each symmFunct
    """

    for timestep in range(len(atoms)):
        print("Calculating timestep " + str(timestep+1))
        for atom in atoms[timestep][0]:
            for funct in symmFuncts:
                funct.call(atom, atoms[timestep][0], atoms[timestep][1]) # index, atomList, box
    for funct in symmFuncts:
        funct.set_info()

def writeBatch(filename, count, pe, symmFuncts, metaIndex, scale_min, scale_max):
    """
    Given a filename, a number of atoms 'count', scaling and location information
    And a collection of symmFuncts with calculated metadata from 'getScalingData'
    This function writes the test batch to the given file
    Given an info array (containing 'funct' number of size-4 array elements),
    updates the [sum, count, min, max] values contributed by this batch
    Note that the values written correspond to the symmetry functions of the atoms

    The updated metadata index is also returned for convenience
    """

    with open(filename, 'w') as f:
        for _ in range(count):
            for funct in xrange(len(symmFuncts)):
                result = symmFuncts[funct].scaled(metaIndex, scale_min, scale_max)
                f.write(str(result) + " ")
            metaIndex += 1
            f.write("\n")
        f.write(str(pe) + "\n")
    return metaIndex


# UPDATE TO SUPPORT MULTIPLE ATOM TYPES
def writeScaling(symmFuncts, info, pe, atomCount, seed, scalingData, nnInfoFile, runnerFolder):
    """
    Given an array of symmetry functions 'symmFuncts'
    The results of applying these symmetry functions to each element in 'info'
    The list of potential energies 'pe'
    And the number of atoms 'atomCount'

    Writes the atom information to "runner/scaling.data"
    And identical symmetry function information to both
    "runner/input.nn" and "runner/input.nn.RuNNer++"

    Details on these outputs can be found in "runner_input.txt" and "runner_input_template.txt"
    """

    defaults = {"verbose" : False}
    data = helper.combine_dicts(scalingData, helper.get_data(nnInfoFile, defaults))
    if data["layers"] == 1:
        data["nodes"] = [data["nodes"]]
        data["activationfunctions"] = [data["activationfunctions"]]
    with open(runnerFolder + "input.nn", "w") as f:
        # Write Settings
        with open("bin/scalingBasics.txt", "r") as fi:
            for line in fi:
                f.write(line)
        f.write("number_of_elements\t1\t# number of elements\n")
        f.write("elements\tC\t# specification of elements\n")
        f.write("random_seed\t" + str(seed) + "\t# seed for initial random weight parameters and train/test splitting\n")
        f.write("cutoff_type\t2\t# type of cutoff function\n")
        f.write("global_hidden_layers_short\t" + str(data["layers"]) + "\t# number of hidden layers\n")
        f.write("global_nodes_short\t" + " ".join(map(str, data["nodes"])) + "\t# number of nodes in hidden layers\n")
        f.write("global_activation_short\t" + " ".join(map(str, data["activationfunctions"])) + " l\t# The activation function used by each layer\n")
        f.write("test_fraction\t" + str(1 - data["trainratio"]) + "\t# threshold for splitting between fitting and test set\n")
        f.write("scale_min_short\t" + str(data["scalemin"]) + "\t# minimum value for scaling\n")
        f.write("scale_max_short\t" + str(data["scalemax"]) + "\t# maximum value for scaling\n")
        f.write("\n")
        
        for funct in symmFuncts:
            f.write(str(funct) + "\n")

    call(["cp", runnerFolder + "input.nn", "runner/input.nn.RuNNer++"])
    
    with open(runnerFolder + "scaling.data", "w") as f:
        # Write Scaling Information
        count = 0
        for i in range(1):
            for j in range(len(symmFuncts)):
                f.write(str(i + 1) + " ")
                f.write(str(j + 1) + " ")
                f.write(symmFuncts[j].data_info())
                f.write("\n")
        f.write(str(sum(pe)/len(pe)/atomCount) + " " + str((max(pe)-min(pe))/atomCount))
        
                
def main():
    if len(sys.argv) < 4:
        print("Give the train/test, symmetry function, and neural network information files")
        return
    # Acquire and read data
    defaults = {"generateData" : True, "trainRatio" : 0.9, "runnerScaling" : "../runner/", "verbose" : False}
    data = helper.get_data(sys.argv[1], defaults)
    verbose = data["verbose"]
    runnerFolder = data["runnerfolder"]
    data_file = data["datafile"]
    if data["generatedata"]:
        print("Generating lammps data")
        if not (data.has_key("lammpsfile") and (data.has_key("seedrange") or data.has_key("seed"))):
            print("Give a lammpsFile and seedRange or seed if you want to generate data")
            return
        if data.has_key("seedrange"):
            seed = random.randint(data["seedrange"][0], data["seedrange"][1])
        else:
            seed = data["seed"]
        generateData(data["lammpsfile"], seed, data_file, runnerFolder)
    
    print("Reading atomic data from " + data_file)
    atomData, thermoData = readAtomData(data_file)
    print("Shuffling data")
    z = list(zip(atomData, thermoData))
    random.shuffle(z)
    atomData, thermoData = zip(*z)

    #Get Functions
    functs = getSymmFunctions(sys.argv[2])
    """functs = []
    # UPDATEEEEEEE
    if isinstance(data["2functions"], list):
        c_temp = ["C" for _ in range(len(data["2functions"]))]
    else:
        c_temp = "C"
    if data.has_key("2functions"):
        functs += get2Functs(data["2functions"], c_temp, c_temp, data["2Rc"], data["2eta"], data["2Rs"])
    if data.has_key("3functions"):
        functs += get3Functs(data["3functions"], c_temp, c_temp, c_temp, data["3Rc"], data["3sigma"], data["3count"])"""
    functs.sort()
    
    # Write train and test files
    trainFolder = data["trainfolder"]
    testFolder = data["testfolder"]
    trainRatio = data["trainratio"]
    trainCutoff = int(trainRatio * len(atomData)) + 1
    i = 0

    should_delete = raw_input("Cleaning (deleting all files) from " + data["trainfolder"] + "  Type 'yes' to confirm:\n")
    if should_delete == "yes":
        # Stolen from: https://stackoverflow.com/questions/185936/delete-folder-contents-in-python
        folder = data["trainfolder"]
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
    should_delete2 = raw_input("Cleaning (deleting all files) from " + data["testfolder"] + "  Type 'yes' to confirm:\n")
    if should_delete2 == "yes":
        folder = data["testfolder"]
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

    print("Calculating scaling metadata for " + str(len(atomData)) + " timesteps")
    getScalingData(atomData, functs)
    print("Writing " + str(trainCutoff) + " training files and " + str(len(atomData)-trainCutoff) + " testing files")
    info = [list([[0, 0, int(1e10), int(-1e10)] for _ in range(len(functs))])]
    metaIndex = 0
    scale_min = data["scalemin"]
    scale_max = data["scalemax"]
    while i < trainCutoff:
        if verbose:
            print("Writing Training Batch: " + str(i+1))
        metaIndex = writeBatch(trainFolder + str(i+1) + ".nndata", len(atomData[i]), thermoData[i], functs, metaIndex, scale_min, scale_max)
        i += 1
    while i < len(atomData):
        if verbose:
            print("Writing Test Batch: " + str(i+1-trainCutoff))
        metaIndex = writeBatch(testFolder + str(i+1-trainCutoff) + ".nndata", len(atomData[i]), thermoData[i], functs, metaIndex, scale_min, scale_max)
        i += 1

    print("Writing function information to scaling.data")
    writeScaling(functs, info, thermoData, len(atomData[0]), seed, data, sys.argv[3], runnerFolder)
        
    
if __name__ == "__main__":
    main()
