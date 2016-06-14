function trainNN(model, batchInputs, batchLabels, epochs, ofile, verbose)
   --[[
      Given a neural network 'nn' with i inputs and o outputs,
      A series of training inputs 'batchInputs' with i column Tensors,
      A series of associated outputs 'batchLabels' with o column Tensors,
      A number of epochs 'epochs' to train over,
      And whether or not training should be 'verbose'
      This function trains and returns nn
   ]]
   
   local criterion = nn.MSECriterion()
   local params, gradParams = model:getParameters()
   local optimState = {learningRate = .01}
   local currentLoss

   for epoch=1,epochs do
      for batch=1,#batchInputs do
	 currentLoss = 0
	 local function feval(params)
	    gradParams:zero()

	    local outputs = model:forward(batchInputs[batch])
	    local loss = criterion:forward(outputs, batchLabels[batch])
	    local dloss_doutput = criterion:backward(outputs, batchLabels[batch])
	    model:backward(batchInputs[batch], dloss_doutput)

	    return loss, gradParams
	 end

	 _,fs = optim.sgd(feval, params, optimState)
	 currentLoss = currentLoss + fs[1]
      end
      if verbose then
	 print("Current Loss = " .. currentLoss)
      end
   end

   return model
end

function testNN(model, testInputs, testLabels, ofile, verbose)
   --[[
      Given a neural network 'nn' with i inputs and o outputs,
      A series of test inputs 'testInputs' with i column Tensors,
      A series of associated outputs 'testLabels' with o column Tensors,
      And whether or not testing should print a percent error for each batch ('verbose'
      This function tests nn with testInputs against testLabels
      And prints the average percent difference between expected and actual results
   ]]
   
   local totalDiff = 0
   for batch=1,#testLabels do
      local batchDiff = 0
      for test=1,(#testLabels[batch])[1] do
	 local expected = testLabels[batch][test][1]
	 local actual = model:forward(testInputs[batch][test])[1]
	 local diff = math.abs((actual-expected)/expected)*100
	 batchDiff = batchDiff + diff
      end
      batchDiff = batchDiff/(#testLabels[batch])[1]
      totalDiff = totalDiff + batchDiff
      if verbose then
	 print("Average percent diff for batch " .. batch .. " = " .. batchDiff .. "%")
      end
   end

   print("\nAverage percent diff for network = " .. (totalDiff/#testLabels) .. "%")
end

