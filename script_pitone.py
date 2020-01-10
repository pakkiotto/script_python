from ruamel.yaml import YAML
from prettytable import PrettyTable
from collections import defaultdict

yaml=YAML(typ='safe')
envs = [ 'JAVA_OPTS', 'TZ', 'NO_PROXY', 'ANCHORS_JWT', 'no_proxy' ]

def flatten_dict(dd, separator ='.', prefix =''):
    if isinstance(dd, dict):
        return { str(prefix) + separator + str(k) if prefix else str(k) : v
             for kk, vv in dd.items()
             for k, v in flatten_dict(vv, separator, kk).items()
             }
    elif isinstance(dd, list):
        return {
            str(prefix) + separator + str(k) if prefix else str(k) : v
            for num, d in enumerate(dd)
            for k,v in flatten_dict(d, separator, '[%s]' % num).items()
        }
    else:
        return { prefix : dd }

def print_diff(dicts, envs, filename):
    dicts = [flatten_dict(d) for d in dicts]
    #UNPACKING OPERATOR IS GOD
    keys = set().union(*dicts)
    x = PrettyTable()
    x.field_names = [filename] + envs
    x.sortby = filename
    for k in keys:
        array = [d.get(k, '-') for d in dicts]
        if(len(set(array))>1):
            array.insert(0,k)
            x.add_row(array)
    print('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>')
    print(x.get_html_string())
def get_data(filename):
    with open(filename, 'r') as f:
        config = yaml.load(f)
        return config['data']
        #Ritorna {k:v}

def compare(filename, environments):
    d = defaultdict(dict)
    for env in environments:
        data = get_data('ocp/' + env + '/' + filename)
        for k, v in data.items():
            d[k][env] = v
    x = PrettyTable()
    x.field_names = ["Name"] + environments
    x.sortby = "Name"
    for k, v in filter(lambda e: e[0] not in envs, d.items()):
        env_vals = [v.get(env, '-') for env in environments]
        # Add only if there's some difference
        if len(set(env_vals)) > 1:
            x.add_row([k] + env_vals)
    print(x.get_html_string())
def compare_yaml(filename, environments):
    str = defaultdict(dict)
    d = defaultdict(dict)
    filenames = set()
    for env in environments:
        #print("\n\nenv " + env)
        data = get_data('ocp/' + env + '/' + filename)
        for cfilename, cfilecontent in data.items():
            #print(cfilename)
            str[env][cfilename] = yaml.load(cfilecontent)
            filenames.add(cfilename)
    for f in filenames:
        dicts = [str.get(env, {}).get(f, '-') for env in environments]
        print_diff(dicts, environments,f)


#compare('journey-env-config-map.yml', ['beapp_DEV', 'beapp_IAT', 'beapp'])
compare_yaml('journey-spring-boot-service.yml', ['beapp_DEV','beapp_IAT', 'beapp'])
'''
def print_diff(d, d2):
    envs = [ 'DICT1','DICT2' ]
    d = flatten_dict(d)
    d2 = flatten_dict(d2)
    keysD = set(d.keys())
    keysD2 = set(d2.keys())
    keys = keysD.union(keysD2)
    x = PrettyTable()
    x.field_names = ["Name"] + envs

    x.sortby = "Name"
    #print(keys)
    for k in keys:
        array = [d.get(k, '-'),d2.get(k, '-')]
        if(len(set(array))>1):
            array.insert(0,k)
            x.add_row(array)
    print(x)
        #Controllare se la key è presente in d e d2 se non c'è in uno riportarla
    #matrice[k][dict1val][dict2val]
'''

    #Controllare se la key è presente in d e d2 se non c'è in uno riportarla
    #matrice[k][dict1val][dict2val]
d = {'a': {'3': 3}, 'c': {'d':{'e':2}}, 'arr': [{'a': 1}, {'a': 2}]}
d2 = {'a': {'3': 4}, 'c': {'d':{'e':2, 'f':'x'}}, 'arr': [{'a': 1}, {'a': 3}], 'l':'f'}
#
envs = ['DICT1', 'DICT2']
dicts = [d,d2]