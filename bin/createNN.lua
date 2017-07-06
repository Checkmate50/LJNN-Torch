require 'bin/nnTrainFiles/nnReqs'
require 'bin/nnTrainFiles/createOptions'

local options = constructCLAOptions()
local CLA = readCLA(arg, options) --CLA = Command Line Arguments
local defaults
defaults, CLA = constructDefaults(CLA)
CLA = addDefaults(CLA, defaults)

if CLA["help"] then
   help()
end

local inputs = CLA["inputs"]
local outputs = CLA["outputs"]
local shouldTrain = not CLA["notrain"]
local trainFolder = CLA["trainfolder"]
local testFolder = CLA["testfolder"]
local trainResults = CLA["trainresults"]
local testResults = CLA["testresults"]
local verbose = CLA["verbose"]
local epochs = CLA["epochs"]
local printFreq = CLA["printfreq"]
local layers = CLA["layers"]
local nodes = CLA["nodes"]
local activationFunctions = CLA["activationfunctions"]
local saveLocation = CLA["save"]
if inputs == nil then
   inputs = inferInputs(trainFolder, outputs)
end
local model = getLinearNN(inputs, outputs, nodes, activationFunctions)
if verbose then
   io.write("Neural Network Created\n")
end

--Attempt to train the model
--[[ This is legacy, only use if you don't want to use the complete main.py package
local trained = false
if shouldTrain then
   model, trained = train(model, inputs, trainFolder, epochs, .01, trainResults, verbose, printFreq)
end
if verbose then
   if trained then
      io.write("Model trained\n\n")
   else
      io.write("No training folder given; model not trained\n")
   end
end

--Test the model if requested
local tested = test(model, inputs, testFolder, testResults, verbose) 
if tested then
   io.write("Model tested\n\n")
else
   io.write("No test folder given; model not tested\n")
end
]]

--Save the model if requested
if saveLocation == nil then
   io.write("Must give save location for model")
else
   torch.save(saveLocation, model)
   if verbose then
      io.write("Model saved to " .. saveLocation .. "\n")
   end
end
