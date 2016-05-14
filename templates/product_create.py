#!/usr/bin/env python
import sys
import yaml
from optparse import OptionParser
from shutil import copyfile
from buildfns_lib import *


def build_site_head(outfile):
    replace_text_with_file_context({'site_head':'contents/site_head.content'}, outfile)

def build_site_navigation(outfile):
    replace_text_with_file_context({'site_navigation':'contents/site_navigation.content'}, outfile)
    #replace_text_with_file_context({'site_navigation':'contents/nav_bar.content'}, outfile)

def build_site_footer(outfile):
    replace_text_with_file_context({'site_footer':'contents/site_footer.content'}, outfile)

def build_prod_jscripts(outfile):
    replace_text_with_file_context({'product_jscript':'contents/prod_jscripts.content'}, outfile)

def build_section_id_product(conf, outfile):
    replace_txt = ''
    if conf['side_prods'].has_key('section_id_bg_img'):
        sid = "id=\"{}\"".format(conf['product'])
        class_ = "class=\"container\""
        style = "style=\"margin-top:-5%; background:url({}) 100% 100% no-repeat; background-size:cover;\"".format(
                            conf['side_prods']['section_id_bg_img'])
        replace_txt = "{} {} {}".format(sid, class_, style)
    else:
        sid = "id=\"{}\"".format(conf['product'])
        class_ = "class=\"container\""
        style = "style=\"margin-top:-5%\""
        replace_txt = "{} {} {}".format(sid, class_, style)

    replace_text({'section-id-product': replace_txt}, outfile)

def build_google_anlytics(outfile):
    replace_text_with_file_context({'google_anlytics':'contents/google_analytics_init.content'}, outfile)


def build_side_prod(side_prod_dict, outfile): 
    side_prods = side_prod_dict['side_prods']
    global function_table
    total_side_txt = ''
    i = 1
    key = 'side_prod{}'.format(i)
    tmp_side_file = '/tmp/sideprod.html'
    total_side_txt = ''
    while key in side_prods:
        if i is 1:
            copyfile('sub_prod_w_sidemenu.html.template', tmp_side_file)
        else:
            copyfile('sub_prod.html.template', tmp_side_file)
        for j in side_prods[key]:
            function_table[j]({j: side_prods[key][j]}, tmp_side_file)

        with open(tmp_side_file, 'r') as f:
            total_side_txt += f.read()

        total_side_txt += '\n'

        i += 1
        key = 'side_prod{}'.format(i)

    replace_text({'side_prods': total_side_txt}, outfile)

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

def main():
    parser = OptionParser()
    parser.add_option("-i", "--schema", dest="infile")
    parser.add_option("-o", "--outfile", dest="outfile")
    (opt, args) = parser.parse_args()

    if not opt.infile:
        print "input file is mandatory!!!"
        parser.print_help()
        return

    conf = yaml.load(open(opt.infile))

    if not opt.outfile:
        outfile = '{}/{}/{}/{}.html'.format(conf['proj_root'], 
                                            conf['hirarchy'],
                                            conf['product'],
                                            conf['product'])

    copyfile('prod.html.template', outfile)

    build_site_head(outfile)
    build_site_navigation(outfile)
    build_site_footer(outfile)
    build_prod_jscripts(outfile)
    #build_google_anlytics(outfile)

    for i in conf:
        if i in function_table:
            function_table[i]({i: conf[i]}, outfile)

    replace_text_with_file_context(
            {'side_prod_menu': '{}_side_proc.menu.content'.format(conf['hirarchy'])},
            outfile)
    build_section_id_product(conf, outfile)

    print outfile + ' is generated'

if __name__ == "__main__":
        sys.exit(main())    # pylint: disable=E1120

