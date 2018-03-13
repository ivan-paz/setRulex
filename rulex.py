from searchPatterns import search_patterns
from writeReadjson import read
from writeReadjson import write
from writeReadjson import clean
from writeReadjson import writePresets
from writeReadjson import readPresets
def dictionary_of_categories(Presets, Rules):
    dictionary_of_classes = dict()
    for preset in Presets:
        preset_class = preset[-1]
        if preset_class not in dictionary_of_classes:
            dictionary_of_classes[preset_class] = [[],[]]
            dictionary_of_classes[preset_class][0].append(preset)
        else:
            dictionary_of_classes[preset_class][0].append(preset)
    for rule in Rules:
        rule_class = rule[-1]
        if rule_class not in dictionary_of_classes:
            dictionary_of_classes[rule_class] = [[],[]]
            dictionary_of_classes[rule_class][1].append(rule)
        else:
            dictionary_of_classes[rule_class][1].append(rule)
    return dictionary_of_classes
#-----------------------------------------------------------------------------
def separate_presets_and_rules_other_categories(key,dictionary_of_classes):
    #Create set with presets of other classes
    presets_other_classes = []
    for key1 in dictionary_of_classes:
        if key1 != key:
            for p in dictionary_of_classes[key1][0]:
                presets_other_classes.append(p)
        else:
            presets_current_class = dictionary_of_classes[key][0]
            rules_current_class = dictionary_of_classes[key][1]
    return [presets_other_classes, presets_current_class, rules_current_class]
#-----------------------------------------------------------------------------
def rulex(Presets, Rules, d, delete_redundant_every_iteration, MEMORYRules):
    final_rules = []
    dictionary_of_classes = dictionary_of_categories(Presets,Rules)
    print(dictionary_of_classes)
    for key in dictionary_of_classes:
        [presets_other_classes,presets_current_class,rules_current_class] = separate_presets_and_rules_other_categories(key,dictionary_of_classes)
        print('key:',key, ';', 'presets other classes : ', presets_other_classes)
        print('search_patterns function')
        [rules,MEMORYRules] = search_patterns(presets_current_class,rules_current_class,presets_other_classes,d,delete_redundant_every_iteration, MEMORYRules)
        for r in rules:
            if r != None:
                final_rules.append(r)
    #print('Final Rules', final_rules)
    return [final_rules, MEMORYRules]

"""
......................................................................
rulex maximum compression function
rewritten as setRulex function
......................................................................
"""
def setRulex(Presets, Rules, d, delete_every_iteration):
    MEMORYpresets = readPresets('MEMORYpresets.json'); print('MEMORYpresets : ',MEMORYpresets)
    MEMORYRules = read('MEMORYRules.json');     print('MEMORYRules : ',MEMORYRules)

    [MEMORYpresets.append(p) for p in Presets if p not in MEMORYpresets];writePresets('MEMORYpresets.json',MEMORYpresets) 
    print('MEMORY PRESETS', MEMORYpresets) 
    if Rules!=[]:
        [Rules.append(r) for r in MEMORYRules] 
    else:
        Rules = MEMORYRules

    print('Rules assigned form MEMORY RULES :  ', Rules)
    previousRules = []
    [rules,MEMORYRules] = rulex(Presets,Rules,d,delete_every_iteration,  MEMORYRules)
    cont = 0
    while rules != previousRules:
        cont +=1
        print('rules != previousRules',cont)
        previousRules = rules
        [rules,MEMORYRules] = rulex(Presets, previousRules, d, delete_every_iteration, MEMORYRules)
    print('Final set of rules extracted with setRulex: ', rules)
    TEMPORAL=[]
    for r in MEMORYRules:
        if r not in TEMPORAL:
            TEMPORAL.append(r)
    MEMORYRules = TEMPORAL 
    write('MEMORYRules.json', MEMORYRules) #----------------------
    print('MEMORYRules at the end of the algorithm :',   MEMORYRules)
    return rules


#clean(all) #clean MEMORY
#Rules = []
#Presets = [[1,2,'*'],           [2,2,'*'], [1,3,'*']]
#Presets = [  [3,2,'*'], [1,4,'*']  ] 

#Presets = [
#        [2,5,'i'],
#        [4,5,'i'],
#        [2,3,'i'],
#        [4,3,'i'],
#        [6,4,'i'],
#        [7,4,'i']
#        ]

#---------------------------------------------------------------------
#print('Example 1 paper fuzzyRulex')
#Rules = []
#clean(all)
#Presets = [[2,2,'coda'],[2,4,'coda']]
#Presets = [[4,2,'coda']]
#rules = setRulex(Presets, Rules, 1, True )
#---------------------------------------------------------------------
print('Example 1 with second order paper fuzzyRulex')
Rules = []
#clean(all)
#Presets = [[4,2,'coda'],[2,2,'coda']]
Presets = [[2,4,'coda']] 
rules = setRulex(Presets, Rules, 1, False )
#---------------------------------------------------------------------



