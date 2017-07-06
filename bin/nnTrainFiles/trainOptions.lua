function constructCLAOptions()
   --[[
      Returns a table listing all command line argument options
      Using the style indicated in readCLA.lua, function readCLA
   ]]

   options = {}

   options["h"] = {"help", false}
   options["trr"] = {"trainresults", true, false, false}
   options["tro"] = {"trainresults", true, false, false}
   options["trainout"] = {"trainresults", true, false, false}
   options["v"] = {"verbose", false}
   options["o"] = {"outputs", true, true, false}
   options["e"] = {"epochs", true, true, false}
   options["lr"] = {"learningrate", true, true, false}
   options["p"] = {"printfreq", true, true, false}
   options["pf"] = {"printfreq", true, true, false}
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
   defaults["criterion"] = "mse"
   defaults["learningrate"] = .01
   defaults["learningratedecay"] = 0
   defaults["weightdecay"] = 0
   defaults["momentum"] = 0
   defaults["epochs"] = 100
   defaults["printfreq"] = 10
   
   return defaults, CLA
end
