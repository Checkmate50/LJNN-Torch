require 'nn'

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
   
if arg[1] == nil or arg[2] == nil then
   io.write("Provide a model and destination file")
end

model = torch.load(arg[1])
io.output(arg[2])

for i=1,#model.modules do
   printTensor(model.modules[i].weight)
   printTensor(model.modules[i].bias)
end

io.output(io.stdout)
