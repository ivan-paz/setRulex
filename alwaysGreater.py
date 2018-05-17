import json
from rulex import setRulex
from writeReadjson import clean
# reads a json file containing sets of presets
with open('presets.json') as json_data:
    setOfPresets = json.load(json_data)

#    rule Extraction
bunch_of_rules = []
d = 1
Rules = [ ]
removeRedundantEveryIteration = False

for Presets in setOfPresets:
    clean(all)
    rules = setRulex(Presets,Rules,1,removeRedundantEveryIteration)
    bunch_of_rules.append(rules)


thefile = open("Output.txt", "w")
for item in bunch_of_rules:
    for rule in item:                                                               
        thefile.write("%s\n" % rule)
    thefile.write("%s\n" % '------------------------------------------')
thefile.close()
