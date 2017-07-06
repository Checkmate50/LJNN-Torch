require 'bin/nnTrainFiles/nnReqs'
require 'bin/nnTrainFiles/trainOptions'

if arg[1] == nil or arg[2] == nil then
   help()
end

local CLA
local trainFolder
local loadLocation
if arg[1] == "-CLA" then
   loadLocation = arg[1]
   trainFolder = arg[2]
   local newArgs = {table.unpack(arg, 3, #arg)}
   local options = constructCLAOptions()
   CLA = readCLA(newArgs, options) --CLA = Command Line Arguments
else
   CLA = readCLA(arg, options)
   if CLA["trainfolder"] == nil or CLA["save"] == nil then
      print("Must give a train folder and save location in nn.info")
      return
   end
   trainFolder = CLA["trainfolder"]
   loadLocation = CLA["save"]
end

local defaults
defaults, CLA = constructDefaults(CLA)
CLA = addDefaults(CLA, defaults)

if CLA["help"] then
   help()
end
local outputs = CLA["outputs"]
local trainResults = CLA["trainresults"]
local testResults = CLA["testresults"]
local verbose = CLA["verbose"]
local epochs = CLA["epochs"]
local criterion = CLA["criterion"]
local lr = CLA["learningrate"]
local lrd = CLA["learningratedecay"]
local wd = CLA["weightdecay"]
local m = CLA["momentum"]
local printFreq = CLA["printfreq"]
local saveLocation = CLA["save"]

if criterion == "mse" then
   criterion = nn.MSECriterion()
else
   io.write("Error, unknown criterion")
   os.exit(1)
end
optimState = {learningRate = lr, learningRateDecay = lrd, weightDecay = wd, momentum = m}

local model = torch.load(loadLocation)

inputs = inferInputs(trainFolder, outputs)
model = train(model, inputs, trainFolder, epochs, criterion, optimState, trainResults, verbose, printFreq)

if saveLocation == nil then
   saveLocation = loadLocation
end

torch.save(saveLocation, model)
io.write("Model saved to " .. saveLocation .. "\n")

