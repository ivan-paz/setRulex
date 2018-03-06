from searchPatterns import search_patterns
from writeReadjson import read
from writeReadjson import write

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


#---    deleting redundant rules after each iteration ----------------
def rulex(Presets, Rules, d, delete_redundant_every_iteration, MEMORYRules):
    final_rules = []
    dictionary_of_classes = dictionary_of_categories(Presets,Rules)
    print(dictionary_of_classes)
    for key in dictionary_of_classes:
        [presets_other_classes,presets_current_class,rules_current_class] = separate_presets_and_rules_other_categories(key,dictionary_of_classes)
        print('key:',key, ';', 'presets other classes : ', presets_other_classes)
        print('search_patterns function')
        #if delete_redundant_every_iteration == False:
        #    rules = search_patterns(presets_current_class,rules_current_class,presets_other_classes, d)
        #else:
        #    rules = search_patterns_delete_redundant(presets_current_class,rules_current_class,presets_other_classes, d)
        [rules,MEMORYRules] = search_patterns(presets_current_class,rules_current_class,presets_other_classes,d,delete_redundant_every_iteration, MEMORYRules)
        for r in rules:
            if r != None:
                final_rules.append(r)
    print('Final Rules', final_rules)
    return [final_rules,MEMORYRules]

"""
......................................................................
rulex maximum compression function
rewritten as setRulex function
......................................................................
"""

def setRulex(Presets,Rules,d,delete_every_iteration):
    MEMORYpresets = read('MEMORYpresets.json');print('MEMORYpresets : ',MEMORYpresets)
    MEMORYRules = read('MEMORYRules.json');print('MEMORYRules : ',MEMORYRules)
    
    if Rules!=[]:
        [Rules.append(r) for r in MEMORYRules] 
    else:
        Rules = MEMORYRules

    previousRules = []
    [rules,MEMORYRules] = rulex(Presets,Rules,d,delete_every_iteration,  MEMORYRules)
    cont = 0
    while rules != previousRules:
        cont +=1
        print('rules != previousRules',cont)
        previousRules = rules
        [rules,MEMORYRules] = rulex(Presets, previousRules, d, delete_every_iteration, MEMORYRules)
    print('final set of rules: ',rules)
    TEMPORAL=[]
    for r in MEMORYRules:
        if r not in TEMPORAL:
            TEMPORAL.append(r)
    MEMORYRules = TEMPORAL 
    #write('MEMORYRules.json', MEMORYRules) #----------------------
    print('memory rules :',   MEMORYRules)
    return rules

Rules = []
Presets = [[1,2,'*'],[2,2,'*'],[1,3,'*']]
#Presets = [
#        [2,5,'i'],
#        [4,5,'i'],
#        [2,3,'i'],
#        [4,3,'i'],
#        [6,4,'i'],
#        [7,4,'i']
#        ]
print('The Presets :  ', Presets)
rules = setRulex(Presets, Rules, 1, False)

print('.............   the end .........................')









