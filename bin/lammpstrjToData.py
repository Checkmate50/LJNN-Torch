#!/usr/local/bin/python
"""
USAGE:
python LAMMPS_to_NNP.py out_filename thermo_filename lammpstrj_filename

Given a thermo file and a split of lammpstrj-styled files
This script creates a compiled data file with the given output file name

Written by Nathan Fox
Edited by Dietrich Geisler
"""
import re
from sys import argv
from math import *
#from enum import Enum
file_num = 0
#this describes 
#class task(Enum):
#  xyz = 1  #this means coordinates and forces are being read in
#  unknown = 2 #look for commans
#  num_atoms = 3

#assume that the write file is correct
def write_header(i):
    out.write("begin\n")  
    out.write("comment Conformation "+ str(i) +"\n")

def print_var(variable):
    for k, v in list(locals().iteritems()):
        if id(v) == id(variable):
            var_name = k
        print var_name +  " = " + variable + "\n"

#the following function will break if multiple spaces are in the beginning of the columns
#searched should be a list
def which_col(searched,search_term):
    i = 0
    done = False
    #  print searched
    for i in range(len(searched)):
        if searched[i].strip() == search_term:
            return i
    print "Could not find " + search_term
    return -1


def print_lattice_basis(a):
    out.write("lattice")
    i = 0
    #  print a
    while i < len(a):
        out.write("   "+ "{:.15e}".format(D_conversion_factor*float(a[i])))
        i+=1
    out.write("\n")


    # lattice parameters for PBC
    #a_x = 0.0
    #b_x = 0.0
    #b_y = 0.0
    #c_x = 0.0
    #c_y = 0.0
    #c_z = 0.0


def lammpstrj_to_data(data_file, thermo_file, lammpstrj_file):
    out = open(argv[1], 'w')
    thermo = open(argv[2], 'r')
    lammpstrj_file = argv[3] # this is without .xyz
    temp = thermo.readline()
    max_nrg = 100.0
    which_run = 1 #this is useful if the first run is not of interest, due to i.e. being an optimization

    #Conversions
    E_conversion_factor = 0.036749309/23.0609 #this is kcal/mol to hartree
    F_conversion_factor = 0.01944689673/23.0609 #this is kcal/mol /angstrom to atomic units of force Hartree/Bohr
    D_conversion_factor = 1.889716164632072 #this is Angstrom to Bohr

    #TO DO DISTANCE CONVERSIONS
    do_forces = True

    current_run = 0
    while current_run != which_run:
        temp = thermo.readline()
        if temp.strip().startswith("Memory usage per processor"):
            current_run += 1

    #temp = thermo.readline()
    temp = thermo.readline()
    args = temp.split()
    #print args

    eng_col = which_col(args,"PotEng")
    a_col = which_col(args,"Cella")
    b_col = which_col(args,"Cellb")
    c_col = which_col(args,"Cellc")
    gamma_col = which_col(args, "CellAlpha") #alpha and gamma are switched because lammps made me do it :-( )-:
    beta_col = which_col(args, "CellBeta") 
    alpha_col = which_col(args, "CellGamma")
    if a_col == -1 or b_col == -1 or c_col == -1 or alpha_col == -1 or beta_col == -1 or gamma_col == -1:
      print_cell = False
    else:
      print_cell = True
    #this is the maximum allowed energy used for training, any conformation above this will not be used

    num_atoms = 0
    curr_tsk = 'unknown'
    conf_num = 1
    xyz_cols_known = False #do we know x y z element fx fy fz
    with open(lammpstrj_file) as lammpstrj_file:
        for line in lammpstrj_file:
            if curr_tsk == 'unknown':
                if line.startswith("ITEM: ATOMS"):
                    if (xyz_cols_known == False):
                        temp = str(line)
                        temp1 = temp.replace("ITEM: ATOMS", "")
                        temp2 = re.sub("\s\s+", " ",temp1).lstrip()
                        args = str(temp2).split()
                        x_col = which_col(args,"x")
                        y_col = which_col(args,"y")
                        z_col = which_col(args,"z")
                        if (do_forces == True):
                            fx_col = which_col(args,"fx")
                            fy_col = which_col(args,"fy")
                            fz_col = which_col(args,"fz")
                        ele_col = which_col(args,"element")
                        #print len(x_col)
                        xyz_cols_known = True
                    curr_tsk = 'xyz'
                    temp1 = re.sub("\s\s+", " ",thermo.readline()).lstrip()
                    temp2 = temp1.split(" ")
                    energy = float(temp2[eng_col])
                    if energy < max_nrg:
                        write_header(conf_num)
                    conf_num+=1
                    if print_cell:
                        a = float(temp2[a_col])
                        b = float(temp2[b_col])
                        c = float(temp2[c_col])
                        alpha = float(temp2[alpha_col])*pi/180
                        beta = float(temp2[beta_col])*pi/180
                        gamma = float(temp2[gamma_col])*pi/180
                        #the following are the cell basis vectors
                        b1 = [a, 0 ,0]
                        b2 = [cos(alpha)*b,sin(alpha)*b,0]
                        b3 = [c*cos(beta),c*(cos(gamma)-cos(beta)*cos(alpha))/sin(alpha)]
                        b3.append(sqrt(c*c-b3[0]*b3[0]-b3[1]*b3[1]))
                        if(b2[1] != 0.0):
                            x_y = b2[0]/b2[1]
                        else:
                            x_y = 0.0
                        if(b2[1]*b3[2] != 0.0):
                            x_z = (b2[1]*b3[0]-b2[0]*b3[1])/(b2[1]*b3[2])
                        else:
                            x_z = 0.0
                        if(b3[2] != 0.0):
                            y_z = b3[1]/b3[2]
                        else:
                            y_z = 0.0

                        print_lattice_basis(b1)
                        print_lattice_basis(b2)
                        print_lattice_basis(b3)
                        #BoOm
                    else:
                        print "Energy of rejected conformation " + str(energy*energy_conversion_factor)
                        curr_tsk= 'skip'
                    #  elif "ITEM: NUMBER OF ATOMS"in line and num_atoms == 0:
                    #    curr_tsk = task['num_atoms']

            elif curr_tsk == 'xyz':
                if line.startswith("ITEM: TIMESTEP"):
                    curr_tsk = 'unknown'
                    charge = 0
                    #temp2 = temp1.split(" ")
                    #print temp2[temp_col]

                    #temp1 = temp2[temp_col]    
                    if(energy >= 0.0):
                        out.write("energy   {:.15e}".format(energy*E_conversion_factor) + "\n")
                    else:
                        out.write("energy  {:.15e}".format(energy*E_conversion_factor) + "\n")
                    if(charge >=0.0):  
                        out.write("charge   {:.15e}".format(charge) + "\n")
                    else:
                        out.write("charge  {:.15e}".format(charge) + "\n")
                    out.write("end\n")
                else:
                    temp = re.sub("\s\s+", " ",line).split()
                    out.write("atom")
                    #these are unconverted because basis vectors are unscaled until print
                    x = float(temp[x_col])
                    y = float(temp[y_col])
                    z = float(temp[z_col])
                    if(z < 0 ):
                        x += b3[0]
                        y += b3[1]
                        z += b3[2]
                    elif(z > b3[2] ):
                        x -= b3[0]
                        y -= b3[1]
                        z -= b3[2]
                    if(y < y_z *z ):
                        x += b2[0]
                        y += b2[1]
                    elif(y > y_z *z + b2[1]):
                        x -= b2[0]
                        y -= b2[1]
                    if(x < x_y * y + x_z * z):
                        x += b1[0]
                    elif(x > x_y * y + x_z * z + b1[0]):
                        x -= b1[0]
                    if do_forces == True:
                        order = [D_conversion_factor*x,D_conversion_factor*y, D_conversion_factor*z,temp[ele_col],0,0,F_conversion_factor*float(temp[fx_col]),F_conversion_factor* float(temp[fy_col]),F_conversion_factor*float(temp[fz_col])  ]
                    else:  
                        order = [D_conversion_factor*x,D_conversion_factor*y, D_conversion_factor*z,temp[ele_col],0,0,0, 0, 0]
                    for i in range(0,len(order)):
                        if order[i] != temp[ele_col]:
                            if float(order[i]) >= 0:
                                out.write(" ")
                            out.write("  {:.15e}".format(float(order[i]) ))
                        else:
                            out.write("   " + order[i] )         
                    out.write("\n")


            elif curr_tsk == 'skip': #for energetically BAD conformations
                if "ITEM: TIMESTEP" in line:
                    curr_tsk = 'unknown'
            #print "Here"
            #out.write("atom  "+ temp[0] + "  "+ temp[1] + "  "+ temp[2] + " He " +"{:.15e}".format(0) + " "+ temp[3] + "  " + temp[4] + "  " + temp[5]+"\n")
    #this is because the last line doesn't make it through apparently


    if(energy >= 0.0):
        out.write("energy   {:.15e}".format(energy*E_conversion_factor) + "\n")
    else:
        out.write("energy  {:.15e}".format(energy*E_conversion_factor) + "\n")
    if(charge >=0.0):
        out.write("charge   {:.15e}".format(charge) + "\n")
    else:
        out.write("charge  {:.15e}".format(charge) + "\n")
    out.write("end\n")

    
def main():
    lammpstrj_to_data(*argv[1:4])

    
if __name__=="__main__":
    main()
