function constructCLAOptions()
   --[[
      Returns a table listing all command line argument options
      Using the style indicated in readCLA.lua, function readCLA
   ]]

   options = {}

   options["h"] = {"help", false}
   options["ter"] = {"testResults", true, false, false}
   options["teo"] = {"testResults", true, false, false}
   options["testout"] = {"testResults", true, false, false}
   options["v"] = {"verbose", false}
   options["o"] = {"outputs", true, true, false}

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
   
   return defaults, CLA
end
