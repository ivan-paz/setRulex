from copy import deepcopy
import itertools
#-------------------------------------------------------------
def preset_into_rule(preset):
    strict_rule = []
    for i in range( len(preset) - 1 ):
        strict_rule.append( set( [ preset[i] ] ) ) #Python 3
    strict_rule.append(preset[-1])                 #Class label
    return strict_rule
#print(preset_into_rule([1,2,3,'A']))
#-------------------------------------------------------------
#   Before  is_compressible
def pattern_found(rule1,rule2, d):
    unions = []
    indexes = []
    difference = 0
    for i in range( len(rule1) - 1 ):
        union = rule1[i] | rule2[i]
        unions.append(union)
        if rule1[i] != rule2[i]:
        #if intersection == set() or len(union) > len(intersection):#Note that this condition is rule formation, it isn't "intersection" between min and max.
            difference +=1
            indexes.append(i)
    if difference <= d: #  GENERAL distance Factor
        return [True, unions, indexes]
    else:
        return [False, None, None]
#print( pattern_found( [{1}, {2}, 'A'], [{2}, {2}, 'A'], 1))
#print( pattern_found([{2}, {2}, 'A'],[{1}, {3}, 'A'],   1))
#print( pattern_found([{1}, {2}, 'A'],[{1}, {2,3},'A'], 1))

def expandRule(rule):
    rules = []
    sets = rule[0:-1]
    #print('sets', sets)
    combinations = itertools.product(*sets)
    for i in combinations:
        temp_rule = []
        combination = i
        #print(combination,type(combination))
        for j in combination:
            _set = set()
            _set.add(j)
            temp_rule.append(_set)
        #for k in rule[-2:]: temp_rule.append(k)
        rules.append(temp_rule)
    #print(rules)
    return rules
#expandRule([{1,2,3},{2,3},'A'])

def contradictions(rule, presets_other_classes):
    rules_other_classes = []
    for p in presets_other_classes:
        rules_other_classes.append(preset_into_rule(p))
    for r in rules_other_classes:
        r = r[0:-1]
    expand = expandRule(rule)
    for r in expand:
        for R in rules_other_classes:
            equal = 0
            for i in range(len(r)):
                if r[i].issubset(R[i]) == True:
                    equal +=1
            if equal == len(r):
                return True #  There are contradiction
    return False # No contradiction
#print(contradictions( [{1,2},{3},'A'], [[1,4,'B'], [4,8,'C'], [1,3,'B']] ))

def create_rule(rule1, unions, indexes, presets_other_classes, d):
    rule = deepcopy(rule1) # D E E P C O P Y 28 SEPT 2017
    for index in indexes:
        rule[index] = unions[index]
    if d >=2:#Here the distance factor is used
        contradiction = contradictions(rule,presets_other_classes)
        if contradiction == False:
            return rule
        else:
            return None
    else:
        return rule
#print( create_rule([{1}, {2}, 'A'],[{2}, {2}, 'A'],  1 )  )
#print( create_rule([{2}, {2}, 'A'],[{1}, {3}, 'A']) )
#print( create_rule([{1}, {2}, 'A'],[{1}, {2,3},'A']))

#  True if a rule1 is subset of rule2, False otherwhise
def contained( rule1, rule2 ):
    #if rule1[-1] == rule2[-1]:
    equalParameters = 0
    for i in range( len(rule1) - 1 ):
        if rule1[i].issubset(rule2[i]):
            equalParameters +=1
    if equalParameters == len(rule1) - 1:
        return True
    else:
        return False
    #else:
    #    return False
# TESTS
#print(contained( [{1},{1},'A'],[{1},{1,2,3},'A']) )
#True
#print(  contained( [{2},{7},'D'],[{2,5},{7},'D']   )   )
#True
def deleteRedundant( rules ):
    for i in range(0, len(rules)):
        redundant = False
        rule1 = rules[i]
        #print('rule1',  rule1)
        for j in range(0, len(rules)):
            rule2 = rules[j]
         #   print(rule2)
            if rule1 != None and rule2 != None and i != j and contained(rule1,rule2) == True:
          #      print(rule1,'contained in', rule2)
                redundant = True
        if redundant == True:
            rules[i] = None
    return rules
# -----    test    -----
#rules = [ [{5}, {5}, 'D', 1], [{2}, {7}, 'D', 1], [{5}, {5, 7}, 'D', 1], [{2, 5}, {7}, 'D', 1] ]


# Search patterns UNIFYED version 25 oct 2017
def search_patterns(presets_current_class, rules_current_class, presets_other_classes, d, delete_redundant_every_iteration, MEMORYRules):
    if delete_redundant_every_iteration == False:    
        print('Removing redundant when iterations are finished!!')
    else:
        print('removing redundant every iteration!!')
    #if not rules_current_class: #Commented 20 NOV
    #    rules_current_class.append( preset_into_rule(presets_current_class[0]) ) #Commented 20 NOV
    for preset in presets_current_class:
       # preset_copy = deepcopy(preset)
        rule_preset = preset_into_rule(preset)
        for i in range(len(rules_current_class)):
            if rules_current_class[i]!=None:
                [pattern,unions,indexes] = pattern_found(rule_preset, rules_current_class[i], d)
                if pattern:
                    rules_current_class.append(create_rule( rule_preset, unions, indexes, presets_other_classes,  d  ))
                    #print('CREATED RULE',create_rule(rule_preset,unions,indexes,presets_other_classes,d))#jajajajajaj
        rules_current_class.append( rule_preset )#preset_into_rule(preset_copy)) # Lo moví de acuerdo con Enrique 20 Nov
        # DELETE D U P L I C A T E D
        rules_current_class=[ii for n,ii in enumerate(rules_current_class) if ii not in rules_current_class[:n]]

        if delete_redundant_every_iteration:
            deleteRedundant(rules_current_class)
            for r in rules_current_class:
                if r!=None:
                    MEMORYRules.append(r)
    if not delete_redundant_every_iteration:
        for r in rules_current_class:
            if r!=None:
                MEMORYRules.append(r)
        deleteRedundant(rules_current_class)

    return [rules_current_class,MEMORYRules]

