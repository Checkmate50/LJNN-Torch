function readCLA(arg, options)
   --[[
      Reads the command line arguments given in arg
      Using the options given by "options"
      Options must give a series of arrays indicating:
      {optionName, hasValue, isNumber, isArray}
      Returns a table indicating the results of this reading
   ]]
   if arg[1] ~= "-CLA" then
      return readFromFiles(arg, options)
   end
   local CLA = {}
   local option, index, number, array
   for i=1,#arg do
      --read next value for designated option
      if option ~= nil then
	 if arg[i]:sub(1,1)=="-" then --Verify that we aren't trying to read in an option
	    CLA["help"] = true
	    return CLA
	 end

	 val = arg[i]
	 if number then val = tonumber(val) end
	 
	 if array then
	    if index == nil then index = 1 end
	    if CLA[option] == nil then CLA[option] = {} end
	    CLA[option][index] = val
	    index = index + 1
	 else
	    CLA[option] = val
	 end

	 if arg[i+1] == nil then
	    break --special case to leave the loop and avoid weird checks
	 elseif not array or arg[i+1]:sub(1,1)=="-" then
	    option = nil
	    index = nil
	 end
	    
      --read next option
      else
	 s = arg[i]:lower() --Ignore case
	 if s:sub(1,2) == "--" then s = s:sub(2,-1) end --Accept options preceeded by both - and --
	 if s:sub(1,1) ~= "-" then  --Check that s is an option preceeded by '-'
	    CLA["help"] = true
	    return CLA
	 end
	 s = s:sub(2,-1) --remove "-" from start of s
	    
	 if options[s] == nil then
	    CLA["help"] = true
	    return CLA
	 end
	 
	 if options[s][2] then
	    option = options[s][1]
	    number = options[s][3]
	    array = options[s][4]
	 else
	    CLA[options[s][1]] = true
	    if s == "help" then
	       return CLA
	    end
	 end
	 
      end
   end
   
   return CLA
end

function readFromFiles(arg)
   --[[
      Given a list of arguments 'arg' of info files to read
      Returns a table of the data stored in these files
   ]]
   local toReturn = {}
   for i = 1,#arg do
      fileData = readFromFile(arg[i])
      for key,value in pairs(fileData) do
	 if toReturn[key] == nil then
	    toReturn[key] = value
	 end
      end
   end
   return toReturn
end

function readFromFile(filename)
   --[[
      Given an info file 'filename'
      Reads the data from that file
      And returns a table of the data (nicely formatted)
   ]]
   local toReturn = {}
   for line in io.lines(filename) do
      sline = {}
      if line == "" or string.sub(line, 1, 1) == "#" then
	 goto continue
      end
      sline = string.split(string.split(line, "#")[1], "%s")
      if #sline == 0 then
	 goto continue
      end
      toAdd = {}
      for i = 1,#sline do
	 if sline[i] ~= "" then
	    temp = tonumber(sline[i])
	    if temp ~= nil then
	       table.insert(toAdd, temp)
	    else
	       table.insert(toAdd, sline[i])
	    end
	 end
      end
      index = toAdd[1]
      table.remove(toAdd, 1)
      if #toAdd == 1 then
	 toReturn[index] = toAdd[1]
      else
	 toReturn[index] = toAdd
      end
      ::continue::
   end
   return toReturn
end
      
function addDefaults(CLA, defaults)
   --[[
      Adds the default options to the given CLA
      Returns the CLA after completion
   ]]

   if CLA["help"] == true then
      return CLA -- If the user requested help, we are done here
   end

   for k, v in pairs(defaults) do
      if CLA[k] == nil then
	 CLA[k] = v
      end
   end

   return CLA
end

function help(message)
   --[[
      Prints the usage for this program and exits
   ]]

   io.write("Calling this file directly is obsolete.  You probably want to run main.py with the correct options.\n")
   io.write("If you insist on calling this script directly, you probably want to run [name_of_script].lua [ttInfoFile].info [nnInfoFile].info.\n")
   io.write("If you really don't want to use this setup, you can take a look at nnTrainFiles/[create {OR} train {OR} test {OR} translate]CLA.lua for each file, respectively, to get an idea for the command line arguments.  If you choose this route, best of luck.\n")
   os.exit()
   
end
