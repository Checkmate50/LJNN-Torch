require 'nnTrainFiles/nnReqs'
require 'nnTrainFiles/trainOptions'

if arg[1] == nil or arg[2] == nil then
   help()
end

local newArgs = {table.unpack(arg, 3, #arg)}
local options = constructCLAOptions()
local CLA = readCLA(newArgs, options) --CLA = Command Line Arguments

local defaults
defaults, CLA = constructDefaults(CLA)
CLA = addDefaults(CLA, defaults)

if CLA["help"] then
   help()
end

local loadLocation = arg[1]
local trainFolder = arg[2]
local inputs = CLA["inputs"]
local outputs = CLA["outputs"]
local trainResults = CLA["train results"]
local testResults = CLA["test results"]
local verbose = CLA["verbose"]
local epochs = CLA["epochs"]
local printFreq = CLA["print freq"]
local saveLocation = CLA["save"]

local model = torch.load(loadLocation)

if inputs == nil then
   inputs = inferInputs(trainFolder, outputs)
end

model = train(model, inputs, trainFolder, epochs, trainResults, verbose, printFreq)

if saveLocation == nil then
   saveLocation = loadLocation
end

torch.save(saveLocation, model)
io.write("Model saved to " .. saveLocation .. "\n")

