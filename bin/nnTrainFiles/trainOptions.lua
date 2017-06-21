function constructCLAOptions()
   --[[
      Returns a table listing all command line argument options
      Using the style indicated in readCLA.lua, function readCLA
   ]]

   options = {}

   options["h"] = {"help", false}
   options["trr"] = {"trainResults", true, false, false}
   options["tro"] = {"trainResults", true, false, false}
   options["trainout"] = {"trainResults", true, false, false}
   options["v"] = {"verbose", false}
   options["o"] = {"outputs", true, true, false}
   options["e"] = {"epochs", true, true, false}
   options["lr"] = {"learningRate", true, true, false}
   options["p"] = {"printFreq", true, true, false}
   options["pf"] = {"printFreq", true, true, false}
   options["s"] = {"save", true, false, false}

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

   defaults["outputs"] = 1
   defaults["verbose"] = false
   defaults["learningRate"] = .01
   defaults["epochs"] = 100
   defaults["printFreq"] = 10
   
   return defaults, CLA
end
