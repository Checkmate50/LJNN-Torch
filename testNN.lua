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
local testFolder = arg[2]
local outputs = CLA["outputs"]
local testResults = CLA["test results"]
local verbose = CLA["verbose"]

local model = torch.load(loadLocation)

inputs = inferInputs(testFolder, outputs)

test(model, inputs, testFolder, testResults, verbose)

