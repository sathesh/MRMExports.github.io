from shutil import copyfile

def replace_text_with_file_context(dict, outfile):
    with open(outfile, 'r') as fout:
        file_text = fout.read()

    search_string = dict.keys()[0]
    replace_file = dict[search_string]
    with open(replace_file, 'r') as rf:
        replace_string = rf.read()

    file_text = file_text.replace('###{}###'.format(search_string), replace_string)

    with open(outfile, 'w') as fout:
        fout.write(file_text)

    return


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


def build_slider(slider_dict, file): 
    slider_data = ''
    for i in slider_dict['slider']:
        slider_data = slider_data + '''<div class="slide"><img src="{}"></div>\n'''.format(i)
    replace_text({'slider':slider_data}, file)
    return


