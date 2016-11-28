function readFile(filepath)
   --[[
      Given a path to a tab-deliminated file 'filepath'
      Returns the data of 'filepath' converted into a table of numbers
      Note that the file cannot contain non-numeric values
   ]]
   local toReturn = {}
   for line in io.lines(filepath) do
      table.insert(toReturn, string.split(line, " "))
   end

   for i=1,#toReturn do
      for j=1,#toReturn[i] do
	toReturn[i][j] = tonumber(toReturn[i][j])
      end
   end

   return toReturn
end

function getBatch(filepath)
   --[[
      Given a path to a tab-deliminated nn training file with numeric values
      Which contains a number of columns equal to inputCount
      And a row at the end indicating the output
      This function returns two values: the tables inputs and output
      Where inputs becomes a fileRowsxinputCount table
      And outputs becomes a fileRowsx(fileColumns-inputCount) table
   ]]
   local data = readFile(filepath)
   local inputs={}
   local outputs = {}

   for i=1,(#data-1) do
      inputs[i] = {}
      for j=1,#data[i] do
	 inputs[i][j] = data[i][j]
      end
   end
   for i=1,#data[#data] do
      outputs[i] = data[#data][i]
   end
   return inputs, outputs
end

function getBatches(folderpath, inputCount)
   --[[
      Given a path to a folder containing a collection of tab-deliminated nn training files
      Each of which contains a table of numeric values such that each table
      Has a number of columns equal to inputCount + [the expected number of outputs]
      This function returns an array of input and output tables
      Note that the files in the given folder must follow the following naming convention:
      folderpath#.txt, where # is an integer such that the first file has # = 1
   ]]
   local i = 1
   local toReturn = {}
   while true do --Only quit when we run out of files
      local s = folderpath .. i .. ".nndata"
      if io.open(s) ~= nil then
	 toReturn[i] = {}
	 toReturn[i][1],toReturn[i][2] = getBatch(s, inputCount)
      else
	 return toReturn
      end
      i = i + 1
   end
   
end

function convertToTensors(batches)
   --[[
      Given a set of n batches of size s with i inputs and o outputs
      Returns two tables of length n
      Where the first table represents inputs with Tensors of size sxi
      And the second table represents outputs with Tensors of size sxo
   ]]
   local inputs = {}
   local outputs = {}

   for i=1,#batches do
      inputs[i]=torch.Tensor(batches[i][1])
      outputs[i]=torch.Tensor(batches[i][2])
   end
   return inputs, outputs
   
end

function getBatchTensors(folderpath, inputCount)
   return convertToTensors(getBatches(folderpath, inputCount))
end

function inferInputs(folderpath)
   local filepath = folderpath .. "1.nndata"
   local line = io.lines(filepath)(1)

   return #(string.split(line, " "))
end
