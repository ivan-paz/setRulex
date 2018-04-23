from searchPatterns import *

from writeReadjson import read
from writeReadjson import write
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

##-------------------------------------------------------------------
##                   Rulex Maximum compression
##-------------------------------------------------------------------
#def dictionary_of_categories(Presets, Rules):
#    dictionary_of_classes = dict()
#    for preset in Presets:
#        preset_class = preset[-1]
#        if preset_class not in dictionary_of_classes:
#            dictionary_of_classes[preset_class] = [[],[]]
#            dictionary_of_classes[preset_class][0].append(preset)
#        else:
#            dictionary_of_classes[preset_class][0].append(preset)
#    for rule in Rules:
#        rule_class = rule[-1]
#        if rule_class not in dictionary_of_classes:
#            dictionary_of_classes[rule_class] = [[],[]]
#            dictionary_of_classes[rule_class][1].append(rule)
#        else:
#            dictionary_of_classes[rule_class][1].append(rule)
#    return dictionary_of_classes
#
#def separate_presets_and_rules_other_categories(key,dictionary_of_classes):
#    #Create set with presets of other classes
#    presets_other_classes = []
#    for key1 in dictionary_of_classes:
#        if key1 != key:
#            for p in dictionary_of_classes[key1][0]:
#                presets_other_classes.append(p)
#        else:
#            presets_current_class = dictionary_of_classes[key][0]
#            rules_current_class = dictionary_of_classes[key][1]
#    return [presets_other_classes, presets_current_class, rules_current_class]
#
#def pattern_found(rule1,rule2, d):
#    unions = []
#    indexes = []
#    difference = 0
#    for i in range( len(rule1) - 1 ):
#        union = rule1[i] | rule2[i]
#        unions.append(union)
#        if rule1[i] != rule2[i]:
#        #if intersection == set() or len(union) > len(intersection):#Note that this condition is rule formation, it isn't "intersection" between min and max.
#            difference +=1
#            indexes.append(i)
#    if difference <= d: #  GENERAL distance Factor
#        return [True, unions, indexes]
#    else:
#        return [False, None, None]
#
#def expandRule(rule):
#    rules = []
#    sets = rule[0:-1]
#    #print('sets', sets)
#    combinations = itertools.product(*sets)
#    for i in combinations:
#        temp_rule = []
#        combination = i
#        #print(combination,type(combination))
#        for j in combination:
#            _set = set()
#            _set.add(j)
#            temp_rule.append(_set)
#        #for k in rule[-2:]: temp_rule.append(k)
#        rules.append(temp_rule)
#    #print(rules)
#    return rules
#expandRule([{1,2,3},{2,3},'A'])
#
#def contradictions(rule, presets_other_classes):
#    rules_other_classes = []
#    for p in presets_other_classes:
#        rules_other_classes.append(preset_into_rule(p))
#    for r in rules_other_classes:
#        r = r[0:-1]
#    expand = expandRule(rule)
#    for r in expand:
#        for R in rules_other_classes:
#            equal = 0
#            for i in range(len(r)):
#                if r[i].issubset(R[i]) == True:
#                    equal +=1
#            if equal == len(r):
#                return True #  There are contradiction
#
#def create_rule(rule1, unions, indexes, presets_other_classes, d):
#    rule = deepcopy(rule1) # D E E P C O P Y 28 SEPT 2017
#    for index in indexes:
#        rule[index] = unions[index]
#    if d >=2:#Here the distance factor is used
#        contradiction = contradictions(rule,presets_other_classes)
#        if contradiction == False:
#            return rule
#        else:
#            return None
#    else:
#        return rule
#
###  True if a rule1 is subset of rule2, False otherwhise
#def contained( rule1, rule2 ):
#    #if rule1[-1] == rule2[-1]:
#    equalParameters = 0
#    for i in range( len(rule1) - 1 ):
#        if rule1[i].issubset(rule2[i]):
#            equalParameters +=1
#    if equalParameters == len(rule1) - 1:
#        return True
#    else:
#        return False
#
#def deleteRedundant( rules ):
#    for i in range(0, len(rules)):
#        redundant = False
#        rule1 = rules[i]
#        #print('rule1',  rule1)
#        for j in range(0, len(rules)):
#            rule2 = rules[j]
#         #   print(rule2)
#            if rule1 != None and rule2 != None and i != j and contained(rule1,rule2) == True:
#          #      print(rule1,'contained in', rule2)
#                redundant = True
#        if redundant == True:
#            rules[i] = None
#    return rules
#
def compressRules(Presets,previousRules,d,delete_every_iteration):
    setOfRules = []
    dictionary = dictionary_of_categories(Presets,previousRules)
    for key in dictionary:
        [presets_other_classes,presets_current_class,rules_current_class] = separate_presets_and_rules_other_categories(key,dictionary)
        print('rules current class',rules_current_class, len(rules_current_class))
        temporalRules = [] #################################################
        for i in range(len(rules_current_class)):
            rule1 = rules_current_class[i]
            for rule2 in temporalRules:##############################setOfRules:
                if rule2!=None: # to avoid comparison with None
                    [pattern,unions,indexes] = pattern_found(rule1,rule2,d)
                    if pattern:
                        rule = create_rule(rule1,unions,indexes,presets_other_classes,d)
                        print('created rule',rule)
                        temporalRules.append(rule)######setOfRules.append(rule)
                    temporalRules=[ii for n,ii in enumerate(temporalRules) if ii not in temporalRules[:n]]
            temporalRules.append(rule1)
        temporalRules = deleteRedundant(temporalRules)
        [setOfRules.append(rule) for rule in temporalRules]
    setOfRules = [x for x in setOfRules if x is not None]
    return setOfRules

#
#def rulexMaxCompress(Presets,Rules,d,delete_every_iteration):
#    previousRules = []
#    rules = rulex(Presets,Rules,d,delete_every_iteration)
#    cont = 0
#    while rules != previousRules:
#        cont +=1
#        print('rules != previousRules',cont)
#        previousRules = rules
#        rules = compressRules(Presets, previousRules, d, delete_every_iteration)
#    print('final set of rules: ',rules)
#    return rules
#
#Rules = []
#Presets = [
#	[2,5,'i'],
#	[4,5,'i'],
#	[2,3,'i'],
#	[4,3,'i'],
#	[6,4,'i'],
#	[7,4,'i']
#	]
#print('The Presets :  ', Presets)
#rules = rulexMaxCompress(Presets, Rules, 1, False)

"""
......................................................................
rulex maximum compression function
rewritten as setRulex function
......................................................................
"""
def setRulex(Presets, Rules, d, delete_every_iteration):
    MEMORYpresets = readPresets('MEMORYpresets.json'); print('MEMORYpresets : ',MEMORYpresets)
    MEMORYRules = read('MEMORYRules.json');            print('MEMORYRules : ',MEMORYRules)

    [MEMORYpresets.append(p) for p in Presets if p not in MEMORYpresets];writePresets('MEMORYpresets.json',MEMORYpresets) 
    print('MEMORY PRESETS', MEMORYpresets)
    [Rules.append(r) for r in MEMORYRules]#this line substitutes the abajo think
    
    print('Rules assigned form MEMORY RULES :  ', Rules)
    previousRules = []
    [rules,MEMORYRules] = rulex(Presets,Rules,d,delete_every_iteration,  MEMORYRules)
    cont = 0
    while rules != previousRules:
        cont +=1
        print('rules != previousRules',cont)
        previousRules = rules
        #[rules,MEMORYRules] = rulex(Presets, previousRules, d, delete_every_iteration, MEMORYRules)
        # necesito que compressRules salve las reglas que va creando en MEMORYRules---------------------------------<<<<<<<
        rules = compressRules(Presets, previousRules, d, delete_every_iteration)
        print('reglas extraidas : ',rules)
    # At this moment the rules created during the compression are not saved
    [MEMORYRules.append(r) for r in rules if r not in MEMORYRules] 
    print('Final set of rules extracted with setRulex: ', rules)
    TEMPORAL=[]
    for r in MEMORYRules:
        if r not in TEMPORAL:
            TEMPORAL.append(r)
    MEMORYRules = TEMPORAL 
    write('MEMORYRules.json', MEMORYRules) #----------------------
    print('MEMORYRules at the end of the algorithm :',   MEMORYRules)
    return rules
