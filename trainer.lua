function trainnn(nn, batchInputs, batchLabels, epochs, verbose)
   local criterion = nn.MSECriterion()

   local params, gradParams = mlp:getParameters()
   local optimState = {learningRate = .01}
   local current_loss

   for epoch=1,epochs do
      for batch=1,#batchInputs do
	 currentLoss = 0
	 local function feval(params)
	    gradParams:zero()

	    local outputs = mlp:forward(batchInputs[batch])
	    local loss = criterion:forward(outputs, batchLabels[batch])
	    local dloss_doutput = criterion:backward(outputs, batchLabels[batch])
	    mlp:backward(batchInputs[batch], dloss_doutput)

	    return loss, gradParams
	 end

	 _,fs = optim.sgd(feval, params, optimState)
	 currentLoss = current_loss + fs[1]
      end
      if verbose then
	 print(currentLoss)
      end
   end

   return nn
end

function testnn(nn, testInputs, testLabels, verbose)
   local totalDiff = 0
   for batch=1,#testLabels do
      local batchDiff = 0
      for test=1,(#testLabels[batch])[1] do
	 local expected = testLabels[batch][test][1]
	 local actual = mlp:forward(testInputs[batch][test])[1]
	 local diff = math.abs((actual-expected)/expected)*100
	 batchDiff = batchDiff + diff
      end
      batchDiff = batchDiff/(#testLabels[batch])[1]
      totalDiff = totalDiff + batchDiff
      if verbose then
	 print("Total percent diff for batch " .. batch .. " = " .. batchDiff)
      end
   end

   print("\nAverage percent diff for network = " .. (totalDiff/#testLabels) .. "%")
end

