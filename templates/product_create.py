#!/usr/bin/env python
import yaml
from shutil import copyfile

conf = yaml.load(open('daal.schema'))

def replace_text(dict,  outfile):
    fin = open(outfile, 'r')
    file_text = fin.read()
    fin.close()

    search_string = dict.keys()[0]
    replace_string = dict[search_string]
    file_text = file_text.replace('###{}###'.format(search_string), replace_string)
    fout = open(outfile, 'w')
    fout.write(file_text)
    fout.close()

    return

def replace_text_multiline(dict,  outfile):
    fin = open(outfile, 'r')
    file_text = fin.read()
    fin.close()

    search_string = dict.keys()[0]
    replace_string = dict[search_string].replace('\n', '<br>')
    file_text = file_text.replace('###{}###'.format(search_string), replace_string)
    fout = open(outfile, 'w')
    fout.write(file_text)
    fout.close()

    return


def build_side_prod(side_prod_dict, file): 
    side_prods = side_prod_dict['side_prods']
    global function_table
    total_side_txt = ''
    i = 1
    key = 'side_prod{}'.format(i)
    tmp_side_file = '/tmp/sideprod.htm'
    total_side_txt = ''
    while key in side_prods:
        copyfile('sub_prod.html.template', tmp_side_file)
        for j in side_prods[key]:
            function_table[j]({j: side_prods[key][j]}, tmp_side_file)

        with open(tmp_side_file, 'r') as f:
            total_side_txt += f.read()

        total_side_txt += '\n'

        i += 1
        key = 'side_prod{}'.format(i)

    replace_text({'side_prods': total_side_txt}, file)

    return

def build_slider(slider_dict, file): 
    slider_data = ''
    for i in slider_dict['slider']:
        slider_data = slider_data + '''<div class="slide"><img src="{}"></div>\n'''.format(i)
    replace_text({'slider':slider_data}, file)
    return

function_table = { 
        'title': replace_text,
        'product': replace_text,
        'prod_desc': replace_text,
        'name': replace_text,
        'desc': replace_text,
        'desc1': replace_text,
        'desc2': replace_text_multiline,
        'image': replace_text,
        'slider': build_slider,
        'side_prods': build_side_prod,
        }

outfile = conf['product']+'.html'
copyfile('prod.html.template', outfile)
for i in conf:
    function_table[i]({i: conf[i]}, outfile)
