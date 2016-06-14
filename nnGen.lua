function getSingleTanhNN(inputs, outputs, HUs, batchFolder, testFolder, epochs, ofile, verbose)
   --[[
      Given a number of 'inputs', 'outputs', and Hidden Layer nodes 'HUs',
      Along with training and testing data in batchFolder and testFolder
      Creates, trains, tests, and returns a single-layered Tanh neural network
   ]]
   
   local model = nn.Sequential()
   model:add(nn.Linear(inputs, HUs))
   model:add(nn.Tanh())
   model:add(nn.Linear(HUs, outputs))
   model = trainTest(model, inputs, batchFolder, testFolder, epochs, ofile, verbose)
   return model
end

function getSingleSigmoidalNN(inputs, outputs, HUs, batchFolder, testFolder, epochs, ofile, verbose)
   --[[
      Given a number of 'inputs', 'outputs', and Hidden Layer nodes 'HUs',
      Along with training and testing data in batchFolder and testFolder
      Creates, trains, tests, and returns a single-layered Sigmoid neural network
   ]]
   
   local model = nn.Sequential()
   model:add(nn.Linear(inputs, HUs))
   model:add(nn.Sigmoid())
   model:add(nn.Linear(HUs, outputs))
   model = trainTest(model, inputs, batchFolder, testFolder, epochs, ofile, verbose)
   return model
end

function trainTest(model, inputs, batchFolder, testFolder, epochs, ofile, verbose)
   --Tests and trains the given model using the given training/testing information
   
   local batchInputs, batchLabels = getBatchTensors(batchFolder, inputs)
   local testInputs, testLabels = getBatchTensors(testFolder, inputs)
   model = trainNN(model, batchInputs, batchLabels, epochs, ofile, verbose)
   testNN(model, testInputs, testLabels, ofile, verbose)
   return model
end
