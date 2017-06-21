require 'bin/nnTrainFiles/nnReqs'

function printTensor(t)
   if t==nil then
      return
   end
   local i
   if ##t==1 then
      for i=1,(#t)[1] do
	 io.write(t[i] .. "\n")
      end
   else
      for i=1,(#t)[1] do
	 printTensor(t[i])
      end
   end
end

local modelLocation
local writeLocation
local shouldWriteRunner = false

if arg[1] == '-CLA' then
   if arg[1] == nil or arg[2] == nil then
      io.write("Provide a model and destination file\n")
   end

   modelLocation = arg[1]
   writeLocation = arg[2]
else
   options = {}
   CLA = readCLA(arg, options)
   modelLocation = CLA['save']
   -- UPDATE POTENTIALLY
   writeLocation = CLA['resultNN']
   shouldWriteRunner = true
end
local model = torch.load(modelLocation)
io.output(writeLocation)

for i=1,#model.modules do
   if model.modules[i].weight == nil then
      goto continue
   end
   printTensor(model.modules[i].weight:t())
   printTensor(model.modules[i].bias)
   ::continue::
end

io.output(io.stdout)
