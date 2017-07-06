function constructCLAOptions()
   --[[
      Returns a table listing all command line argument options
      Using the style indicated in readCLA.lua, function readCLA
   ]]

   options = {}

   options["h"] = {"help", false}
   options["tr"] = {"trainfolder", true, false, false}
   options["train"] = {"trainfolder", true, false, false}
   options["te"] = {"testfolder", true, false, false}
   options["test"] = {"testfolder", true, false, false}
   options["trr"] = {"trainresults", true, false, false}
   options["tro"] = {"trainresults", true, false, false}
   options["trainout"] = {"trainresults", true, false, false}
   options["ter"] = {"testresults", true, false, false}
   options["teo"] = {"testresults", true, false, false}
   options["testout"] = {"testresults", true, false, false}
   options["nt"] = {"notrain", false}
   options["notrain"] = {"notrain", false}
   options["v"] = {"verbose", false}
   options["o"] = {"outputs", true, true, false}
   options["e"] = {"epochs", true, true, false}
   options["p"] = {"printfreq", true, true, false}
   options["pf"] = {"printfreq", true, true, false}
   options["l"] = {"layers", true, true, false, false}
   options["lc"] = {"layers", true, true, false, false}
   options["n"] = {"nodes", true, true, true}
   options["n"] = {"nodes", true, true, true}
   options["lt"] = {"activationfunctions", true, false, true}
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
   if CLA["inputs"] == nil and CLA["trainfolder"] == nil then
      print("trainfolder is a required variable")
      return defaults, CLA
   end

   defaults["outputs"] = 1
   defaults["norrain"] = false
   defaults["verbose"] = false
   defaults["epochs"] = 100
   defaults["printfreq"] = 10
   if CLA["layers"] == nil then CLA["layers"] = 1 end
   if CLA["nodes"] == nil then CLA["nodes"] = {} end
   if CLA["activationfunctions"] == nil then CLA["activationfunctions"] = {} end

   if type(CLA["nodes"]) ~= "table" then
      temp = {}
      table.insert(temp, CLA["nodes"])
      CLA["nodes"] = temp
      temp = {}
      table.insert(temp, CLA["activationfunctions"])
      CLA["activationfunctions"] = temp
   end

   if #(CLA["nodes"]) ~= CLA["layers"] or #(CLA["activationfunctions"]) ~= CLA["layers"] then
      print("The number of nodes and activationFunctions listed must match the number of layers listed")
   end
   
   return defaults, CLA
end
