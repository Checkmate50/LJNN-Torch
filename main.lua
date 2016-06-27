require 'trainReqs'

local inputs = 3
local outputs = 1
local batchFolder = "trainBatches/"
local testFolder = "testBatches/"
local trainFile = "train.txt"
local testfile = "tests.txt"

local model = getSingleTanhNN(inputs, outputs, 20)
model = train(model, inputs, batchFolder, 100, trainFile, false, 10)
test(model, inputs, testFolder, testFile, false)

torch.save("model.net", model)
