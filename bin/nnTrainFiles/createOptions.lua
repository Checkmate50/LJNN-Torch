function constructCLAOptions()
   --[[
      Returns a table listing all command line argument options
      Using the style indicated in readCLA.lua, function readCLA
   ]]

   options = {}

   options["h"] = {"help", false}
   options["tr"] = {"train folder", true, false, false}
   options["train"] = {"train folder", true, false, false}
   options["te"] = {"test folder", true, false, false}
   options["test"] = {"test folder", true, false, false}
   options["trr"] = {"train results", true, false, false}
   options["tro"] = {"train results", true, false, false}
   options["trainout"] = {"train results", true, false, false}
   options["ter"] = {"test results", true, false, false}
   options["teo"] = {"test results", true, false, false}
   options["testout"] = {"test results", true, false, false}
   options["nt"] = {"no train", false}
   options["notrain"] = {"no train", false}
   options["v"] = {"verbose", false}
   options["o"] = {"outputs", true, true, false}
   options["e"] = {"epochs", true, true, false}
   options["p"] = {"print freq", true, true, false}
   options["pf"] = {"print freq", true, true, false}
   options["l"] = {"level count", true, true, false, false}
   options["lc"] = {"level count", true, true, false, false}
   options["hu"] = {"HUs", true, true, true}
   options["hn"] = {"HUs", true, true, true}
   options["lt"] = {"level types", true, false, true}
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
   if CLA["inputs"] == nil and CLA["train folder"] == nil then
      CLA["help"] = true
      return defaults, CLA
   end

   defaults["outputs"] = 1
   defaults["no train"] = false
   defaults["verbose"] = false
   defaults["epochs"] = 100
   defaults["print freq"] = 10
   if CLA["level count"] == nil then CLA["level count"] = 1 end
   if CLA["HUs"] == nil then CLA["HUs"] = {} end
   if CLA["level types"] == nil then CLA["level types"] = {} end

   local index = #(CLA["HUs"])+1
   while index <= CLA["level count"] do
      CLA["HUs"][index] = 20
      index = index + 1
   end

   index = #(CLA["level types"])+1
   while index <= CLA["level count"] do
      CLA["level types"][index] = "t"
      index = index + 1
   end

   for i=1,#CLA["level types"] do
      CLA["level types"][i] = string.lower(CLA["level types"][i])
   end

   if #(CLA["HUs"]) > CLA["level count"] or #(CLA["level types"]) > CLA["level count"] then
      CLA["help"] = true
   end
   
   return defaults, CLA
end
