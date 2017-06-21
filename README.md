# LJNN-Torch

This framework allows for the generation of data for training a feed-forward neural network which can be used for extending MD simulations.

Home Github: https://github.com/Checkmate50/LJNN-Torch

Written by Dietrich Geisler

Last Updated 6/21/2017

###########################################
#               Simple Use                #
###########################################

Install Python2 and specify the run command in main.info under the python data field

Install lammps with the pair_runner.cpp/pair_runner.h extensions.  Specify the run command in tt.info under the lammps data field

run main.py with python2 to run the framework!
(e.g. python main.py)

If using the torch library for neural network training, install lua and torch and specify the run command in main.py under the torch data field

###########################################
#               Info Files                #
###########################################

The following info files contain modifiable information that is needed by the framework when making decisions:

main.info

tt.info

symmFuncts.info

nn.info


You can change the values in these files to change the behavior of simulations or add your own modules (see the section on adding modules for details on performing the latter).  The data field is on the left and the data is a series of whitespace delimited values on the right.  Comments are preceeded with a '#'.  Data fields are not case-sensitive.

Data fields that are not recognized by bin/verifyInfo.py give a warning if they are added.  Missing data fields give an error and quit the framework if they are required.  If verbosity is enabled, optional data fields give a notification if they are empty.  Data fields with the incorrect data type give an error and quit the framework.

The info files may be updated by software to match expected case, so make sure they aren't write-protected to avoid unexpected behavior

If you want to add expected/required data fields, modify bin/verifyInfo.py directly (see the code documentation on how to do so).

###########################################
#             Required Files              #
###########################################

WARNING: Do not delete the following files unless you know what you're doing!  You may need to use or update these files if you want to add features or support for things, just don't change/delete exisiting code if you can help it.

main.py

bin/helper.py

bin/updateNN.py

bin/verifyInfo.py

###########################################
#            Acknowledgemenets            #
###########################################

Nathan Fox for helping me work through RuNNer and design the framework

Michael Grunwald for being an awesome advisor

Andreas Singraber for making the RuNNer++ framework

Hope this code helps you out, good luck!  Let me know via github if you have any issues; I'm planning to maintain this code at least until 2020.