function constructCLAOptions()
   --[[
      Returns a table listing all command line argument options
      Using the style indicated in readCLA.lua, function readCLA
   ]]

   options = {}

   options["h"] = {"help", false}
   options["tr"] = {"trainFolder", true, false, false}
   options["train"] = {"trainFolder", true, false, false}
   options["te"] = {"testFolder", true, false, false}
   options["test"] = {"testFolder", true, false, false}
   options["trr"] = {"trainResults", true, false, false}
   options["tro"] = {"trainResults", true, false, false}
   options["trainout"] = {"trainResults", true, false, false}
   options["ter"] = {"testResults", true, false, false}
   options["teo"] = {"testResults", true, false, false}
   options["testout"] = {"testResults", true, false, false}
   options["nt"] = {"noTrain", false}
   options["notrain"] = {"noTrain", false}
   options["v"] = {"verbose", false}
   options["o"] = {"outputs", true, true, false}
   options["e"] = {"epochs", true, true, false}
   options["p"] = {"printFreq", true, true, false}
   options["pf"] = {"printFreq", true, true, false}
   options["l"] = {"layers", true, true, false, false}
   options["lc"] = {"layers", true, true, false, false}
   options["n"] = {"nodes", true, true, true}
   options["n"] = {"nodes", true, true, true}
   options["lt"] = {"activationFunctions", true, false, true}
   options["s"] = {"save", true, false, false}
   options["i"] = {"inputs", true, true, false}

   return options
end

function constructDefaults(CLA)
   --[[
      Given the command line arguments "CLA"
      Returns the modified CLA and a table listing all option defaults
      Using the style indicated in readCLA.lua, function addDefaults
   ]]

   defaults = {}

   if CLA["help"] then
      return defaults, CLA
   end
   if CLA["inputs"] == nil and CLA["trainFolder"] == nil then
      print("trainFolder is a required variable")
      return defaults, CLA
   end

   defaults["outputs"] = 1
   defaults["noTrain"] = false
   defaults["verbose"] = false
   defaults["epochs"] = 100
   defaults["printFreq"] = 10
   if CLA["layers"] == nil then CLA["layers"] = 1 end
   if CLA["nodes"] == nil then CLA["nodes"] = {} end
   if CLA["activationFunctions"] == nil then CLA["activationFunctions"] = {} end

   if type(CLA["nodes"]) ~= "table" then
      temp = {}
      table.insert(temp, CLA["nodes"])
      CLA["nodes"] = temp
      temp = {}
      table.insert(temp, CLA["activationFunctions"])
      CLA["activationFunctions"] = temp
   end

   if #(CLA["nodes"]) ~= CLA["layers"] or #(CLA["activationFunctions"]) ~= CLA["layers"] then
      print("The number of nodes and activationFunctions listed must match the number of layers listed")
   end
   
   return defaults, CLA
end
