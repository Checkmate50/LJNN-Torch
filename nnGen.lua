function getSingleTanhNN(inputs, outputs, HUs)
   --[[
      Given a number of 'inputs', 'outputs', and Hidden Layer nodes 'HUs',
      Along with training and testing data in batchFolder and testFolder
      Creates, trains, tests, and returns a single-layered Tanh neural network
   ]]
   
   local model = nn.Sequential()
   model:add(nn.Linear(inputs, HUs))
   model:add(nn.Tanh())
   model:add(nn.Linear(HUs, outputs))
   return model
end

function getSingleSigmoidalNN(inputs, outputs, HUs)
   --[[
      Given a number of 'inputs', 'outputs', and Hidden Layer nodes 'HUs',
      Along with training and testing data in batchFolder and testFolder
      Creates, trains, tests, and returns a single-layered Sigmoid neural network
   ]]
   
   local model = nn.Sequential()
   model:add(nn.Linear(inputs, HUs))
   model:add(nn.Sigmoid())
   model:add(nn.Linear(HUs, outputs))
   return model
end

function train(model, inputs, batchFolder, epochs, ofile, verbose, printFreq)
   --Retrieves the batches from the given folder and trains the given model using the given information
   --Returns the model after testing is completed

   local batchInputs, batchLabels = getBatchTensors(batchFolder, inputs)
   model = trainNN(model, batchInputs, batchLabels, epochs, ofile, verbose, printFreq)
   return model
end

function test(model, inputs, testFolder, ofile, verbose)
   --Retrieves the tests from the given folder and tests the given model using the given information
   
   local testInputs, testLabels = getBatchTensors(testFolder, inputs)
   testNN(model, testInputs, testLabels, ofile, verbose)
end
