import json
def read(file_name):
    with open(file_name) as json_data:
        file_content = json.load(json_data)
        return file_content

def write(file_name,data):
    with open (file_name, 'w') as f:
        json.dump(data,f)
#--------------------------------------
def clean_all():
    files= ['all_connected_sets.json','connected_rules_indexes.json', 'lonly_rules.json','lonly_rules_indexes.json','optimum_partitions.json']
    for file in files: write(file,[])
#clean_all()

