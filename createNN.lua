require 'nnTrainFiles/nnReqs'
require 'nnTrainFiles/createOptions'

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
local shouldTrain = not CLA["no train"]
local trainFolder = CLA["train folder"]
local testFolder = CLA["test folder"]
local trainResults = CLA["train results"]
local testResults = CLA["test results"]
local verbose = CLA["verbose"]
local epochs = CLA["epochs"]
local printFreq = CLA["print freq"]
local levelCount = CLA["level count"]
local HUs = CLA["HUs"]
local levelTypes = CLA["level types"]
local saveLocation = CLA["save"]

if inputs == nil then
   inputs = inferInputs(trainFolder, outputs)
end
local model = getLinearNN(inputs, outputs, HUs, levelTypes)
io.write("Model created\n\n")

--Attempt to train the model
local trained = false
if shouldTrain then
   model, trained = train(model, inputs, trainFolder, epochs, .01, trainResults, verbose, printFreq)
end
if trained then
   io.write("Model trained\n\n")
else
   io.write("No training folder given; model not trained\n")
end

--Test the model if requested
local tested = test(model, inputs, testFolder, testResults, verbose) 
if tested then
   io.write("Model tested\n\n")
else
   io.write("No test folder given; model not tested\n")
end

--Save the model if requested
if saveLocation == nil then
   io.write("No save file given; model not saved\n")
else
   torch.save(saveLocation, model)
   io.write("Model saved to " .. saveLocation .. "\n")
end
