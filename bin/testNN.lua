require 'bin/nnTrainFiles/nnReqs'
require 'bin/nnTrainFiles/testOptions'

if arg[1] == nil or arg[2] == nil then
   help()
end

local CLA
local trainFolder
local loadLocation
if arg[1] == "-CLA" then
   loadLocation = arg[1]
   testFolder = arg[2]
   local newArgs = {table.unpack(arg, 3, #arg)}
   local options = constructCLAOptions()
   CLA = readCLA(newArgs, options) --CLA = Command Line Arguments
else
   CLA = readCLA(arg, options)
   if CLA["trainfolder"] == nil or CLA["save"] == nil then
      print("Must give a train folder and save location in nn.info")
      return
   end
   testFolder = CLA["testfolder"]
   loadLocation = CLA["save"]
end

local defaults
defaults, CLA = constructDefaults(CLA)
CLA = addDefaults(CLA, defaults)

if CLA["help"] then
   help()
end

local outputs = CLA["outputs"]
local testResults = CLA["testresults"]
local verbose = CLA["verbose"]

local model = torch.load(loadLocation)

inputs = inferInputs(testFolder, outputs)

test(model, inputs, testFolder, testResults, verbose)

