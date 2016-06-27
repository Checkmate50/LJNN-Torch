require 'trainReqs'

local inputs = 3
local outputs = 1
local batchFolder = "trainBatches/"
local testFolder = "testBatches/"
local trainFile = "train.txt"
local testFile = "tests.txt"

local model = getSingleTanhNN(inputs, outputs, 20)
io.write("Model created\n")
model = train(model, inputs, batchFolder, 100, trainFile, true, 10)
io.write("Model trained\n")
test(model, inputs, testFolder, testFile, true)
io.write("Model tested\n")

torch.save("model.net", model)
