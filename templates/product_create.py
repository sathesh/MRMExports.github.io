import yaml
import re
from shutil import copyfile

conf = yaml.load(open('daal.schema'))

def replace_text(dict,  file):
    fin = open(outfile, 'r')
    file_text = fin.read()
    fin.close()

    search_string = dict.keys()[0]
    replace_string = dict[search_string]
    file_text = file_text.replace('###{}###'.format(search_string), replace_string)
    fout = open(outfile, 'w')
    fout.write(file_text)

    return

def build_side_prod(side_prod_dict, file): 
    return

def build_slider(side_prod_dict, file): 
    return

function_table = { 
        'title': replace_text,
        'product': replace_text,
        'prod_desc': replace_text,
        'name': replace_text,
        'desc1': replace_text,
        'desc2': replace_text,
        'image': replace_text,
        'slider': build_slider,
        'side_prods': build_side_prod,
        }

outfile = conf['product']+'.html'
copyfile('prod.html.template', outfile)
for i in conf:
    function_table[i]({i: conf[i]}, outfile)
