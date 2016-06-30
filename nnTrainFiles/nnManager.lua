function getLinearNN(inputs, outputs, HUs, levelTypes)
   --[[
      Given a number of nn 'inputs'
      A number of nn 'outputs'
      A number of 'levels' of hidden layers
      A table of the number of hidden nodes per level 'HUs'
      And the connection type of each layer 'levels'
      returns a sequential model meeting these specifications
      (Note that the only supported connections are t=tanh and s=sigmoid)
   ]]

   local model = nn.Sequential()
   table.insert(HUs, outputs)
   model:add(nn.Linear(inputs, HUs[1]))
   local final = #HUs-1
   for i=1,final do
      if levelTypes[i] == "t" then
	 model:add(nn.Tanh())
      elseif levelTypes[i] == "s" then
	 model:add(nn.Sigmoid())
      else
	 io.write("Level Type " .. levelTypes[i] .. " not supported\n")
	 os.exit()
      end

      model:add(nn.Linear(HUs[i], HUs[i+1]))
   end
   return model
end

function train(model, inputs, batchFolder, epochs, ofilepath, verbose, printFreq)
   --Retrieves the batches from the given folder and trains the given model using the given information
   --Returns the model after testing is completed

   if batchFolder == nil then
      return model, false
   end
   local batchInputs, batchLabels = getBatchTensors(batchFolder, inputs)
   model = trainNN(model, batchInputs, batchLabels, epochs, ofilepath, verbose, printFreq)
   return model, true
end

function test(model, inputs, testFolder, ofilepath, verbose)
   --Retrieves the tests from the given folder and tests the given model using the given information

   if testFolder == nil then
      return false
   end
   local testInputs, testLabels = getBatchTensors(testFolder, inputs)
   testNN(model, testInputs, testLabels, ofilepath, verbose)
   return true
end
