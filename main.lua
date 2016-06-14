require 'trainReqs'

local inputs = 3
local outputs = 1
local batchFolder = "trainBatches/"
local testFolder = "testBatches/"
local outputFile = "output.txt"
local model = getSingleTanhNN(inputs, outputs, 20, batchFolder, testFolder, 100, outputFile, true)

torch.save("model.net", model)
