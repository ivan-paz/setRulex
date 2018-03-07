import json

def read(file_name):
    with open(file_name) as json_data:
        file_content = json.load(json_data)
    temporalData = []
    for r in file_content:
        rule = []
        for p in range(len(r)-1):
            rule.append(set(r[p]))
        rule.append(r[-1])
        temporalData.append(rule)
    file_content = temporalData
    return file_content

def write(file_name,data):
    temporalData = []
    for r in data:
        rule = []
        for p in range( len(r) - 1):
            rule.append(list(r[p]))
        rule.append(r[-1])
        temporalData.append(rule)
    data = temporalData
    with open (file_name, 'w') as f:
        json.dump(data,f)
#write('MEMORYRules.json',[[ {1},{2,3}, '*'], [{3}, {1}, 'A']])
#read('MEMORYRules.json')

def writePresets(file_name,data):
    with open(file_name, 'w') as f:
        json.dump(data,f)

def readPresets(file_name):
    with open(file_name) as json_data:
        file_content = json.load(json_data)
    return file_content

def clean(_files):
    if _files == all:
        files= ['MEMORYpresets.json','MEMORYRules.json']
    else:
        [files.append(f) for f in _files]
    for file in files: write(file,[])
