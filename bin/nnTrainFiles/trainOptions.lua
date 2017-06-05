function constructCLAOptions()
   --[[
      Returns a table listing all command line argument options
      Using the style indicated in readCLA.lua, function readCLA
   ]]

   options = {}

   options["h"] = {"help", false}
   options["trr"] = {"train results", true, false, false}
   options["tro"] = {"train results", true, false, false}
   options["trainout"] = {"train results", true, false, false}
   options["v"] = {"verbose", false}
   options["o"] = {"outputs", true, true, false}
   options["e"] = {"epochs", true, true, false}
   options["lr"] = {"learning rate", true, true, false}
   options["p"] = {"print freq", true, true, false}
   options["pf"] = {"print freq", true, true, false}
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
   defaults["learning rate"] = .01
   defaults["epochs"] = 100
   defaults["print freq"] = 10
   
   return defaults, CLA
end
