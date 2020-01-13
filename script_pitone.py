from ruamel.yaml import YAML
from prettytable import PrettyTable
from collections import defaultdict
from random import randint

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
    randID = randint(100, 999)
    print('<div class= "container row"><div class="col s12"><div data-id='+filename+str(randID)+' onclick="showhidetable()" class="btn-flat btn-large">Show or hide the resume table with difference of the file ' + filename +'</div></div></div>')
    print('<div class="row" id='+filename+str(randID)+' style="display:none;" ><div class="col s12"><div class="card white">')
    print(x.get_html_string())
    print('</div></div></div>')
def get_data(filename):
    with open(filename, 'r') as f:
        config = yaml.load(f)
        return config['data']
        #Ritorna {k:v}

def compare(filename, environments):
    print('<div class="container"><div class="row"><div class="card-panel grey darken-4 center"><span class="white-text text-white">This is a resume table with difference of the file journey-env-config map in the openshift envirionments</span></div></div></div>')
    d = defaultdict(dict)
    for env in environments:
        data = get_data('ocp/' + env + '/' + filename)
        for k, v in data.items():
            d[k][env] = v
    x = PrettyTable()
    x.field_names = ["journey-env-config-map"] + environments
    x.sortby = "journey-env-config-map"
    for k, v in filter(lambda e: e[0] not in envs, d.items()):
        env_vals = [v.get(env, '-') for env in environments]
        # Add only if there's some difference
        if len(set(env_vals)) > 1:
            x.add_row([k] + env_vals)
    randID = randint(100, 999)
    print('<div class= "container row"><div class="col s12"><div data-id='+filename+str(randID)+' onclick="showhidetable()" class="btn-flat btn-large">Show or hide the resume table with difference of the file ' + filename +'</div></div></div>')
    print('<div class="row" id='+filename+str(randID)+'  style="display:none;"><div class="col s12 "><div class="card white">')
    print(x.get_html_string())
    print('</div></div></div>')

def compare_yaml(filename, environments):
    print('<div class="container"><div class="row"><div class="card-panel grey darken-4 center"><span class="white-text text-white">This is a resume table with difference of the file journey-spring-boot-service.yml yaml in the openshift envirionments</span></div></div></div>')
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

print('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script><h2 class="header center">Resume of config map and envirionments variables of DXL</h2>')
compare('journey-env-config-map.yml', ['beapp_DEV', 'beapp_IAT', 'beapp'])
compare_yaml('journey-spring-boot-service.yml', ['beapp_DEV','beapp_IAT', 'beapp'])
print('<script type="text/javascript">function showhidetable(){var id=event.target.getAttribute("data-id");var style = document.getElementById(id).style.display;if(style == "none"){document.getElementById(id).style.display = "block"}else{document.getElementById(id).style.display = "none"}};document.querySelectorAll("table").forEach( (element) => { if(element != undefined){ element.className = "highlight  responsive-table"} } ); var tables = document.querySelectorAll("table");for (i = 0; i< tables.length ; i++){var header = document.createElement("thead");oldhtml = tables[i].childNodes[1].firstChild.innerHTML;tables[i].childNodes[1].firstChild.innerHTML = "";header.innerHTML =  oldhtml;tables[i].appendChild(header);};document.querySelectorAll("td").forEach((e) => {e.innerHTML= e.innerHTML.replace(/(.{50})/g, "$1<br>");})</script>')
