function sumTensor(t) --currently unused
   local result = torch.Tensor(1, (#t)[2])
   for i=1,(#t)[2] do
      local sum = 0
      for j=1,(#t)[1] do
	 sum = sum + t[j][i]
      end
      result[i] = sum
   end
   return result
end

function splitTensor(t, count)
   local results = torch.Tensor(count, (#t)[1])
   for i=1,(#t)[1] do
      local num = t[i]/count
      for j=1,count do
	 results[j][i] = num
      end
   end
   return results
end

function trainNN(model, batchInputs, batchLabels, epochs, lr, ofilepath, verbose, printFreq)
   --[[
      Given a neural network 'model' with:
      A series of training inputs 'batchInputs' with i column Tensors,
      A series of associated outputs 'batchLabels' with o column Tensors,
      A number of epochs 'epochs' to train over,
      A learning rate 'lr'
      Whether or not training should be 'verbose',
      The file to write to 'ofilepath' (if this is nil, writes to console)
      And a frequency at which to print model state
      This function trains and returns nn
   ]]
   
   local criterion = nn.MSECriterion()
   local params, gradParams = model:getParameters()
   local optimState = {learningRate = lr}
   if ofilepath ~= nil then
      io.output(ofilepath)
   end
   local currentLoss

   for epoch=1,epochs do
      for batch=1,#batchInputs do
	 currentLoss = 0
	 local function feval(params)
	    gradParams:zero()
	    local outputs = model:forward(batchInputs[batch])
	    local split_labels = splitTensor(batchLabels[batch], (#batchInputs[batch])[1])
	    local loss = criterion:forward(outputs, split_labels)
	    local dloss_doutput = criterion:backward(outputs, split_labels)
	    model:backward(batchInputs[batch], dloss_doutput)

	    return loss, gradParams
	 end

	 _,fs = optim.sgd(feval, params, optimState)
	 currentLoss = currentLoss + fs[1]
      end
      if epoch % printFreq == 0 then
	 if verbose then
	    io.write("Epoch " .. epoch .. "\t")
	 end
	 io.write("Current Loss = " .. currentLoss .. "\n")
      end
   end

   io.write("\n")
   io.output(io.stdout)
   return model
end

function testNN(model, testInputs, testLabels, ofilepath, verbose)
   --[[
      Given a neural network 'nn' with i inputs and o outputs,
      A series of test inputs 'testInputs' with i column Tensors,
      A series of associated outputs 'testLabels' with o column Tensors,
      Whether or not testing should print a percent error for each batch ('verbose')
      And the file to write to 'ofilepath' (if this is nil, writes to console)
      This function tests nn with testInputs against testLabels
      And prints the average percent difference between expected and actual results
   ]]
   
   local totalDiff = 0
   if ofilepath ~= nil then
      io.output(ofilepath)
   end
   
   for batch=1,#testLabels do
      local batchDiff = 0
      local expected = testLabels[batch][1]
      local result = model:forward(testInputs[batch])
      local actual = sumTensor(result)[1][1]
      local diff = math.abs((actual-expected)/expected)*100
      batchDiff = diff/(#testLabels[batch])[1]
      totalDiff = totalDiff + batchDiff
      if verbose then
	 io.write("Average percent diff for batch " .. batch .. " = " .. batchDiff .. "%\n")
      end
   end

   if verbose then
      io.write("\n")
   end
   io.write("Average percent diff for network = " .. (totalDiff/#testLabels) .. "%\n")

   io.output(io.stdout)
end

