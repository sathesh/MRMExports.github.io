#!/usr/bin/env python
import sys
import os
import yaml
from optparse import OptionParser
from shutil import copyfile
from buildfns_lib import *
from config import *

def set_active_menu(menu, outfile):
    return

def build_site_head(outfile):
    replace_text_with_file_context({'site_head':SITE_HEAD_FILE}, outfile)

def build_site_navigation(menu, outfile):
    replace_text_with_file_context({'site_navigation':SITE_NAVIGATION_FILE}, outfile)
    set_active_menu(menu, outfile)

def build_site_footer(outfile):
    replace_text_with_file_context({'site_footer':SITE_FOOTER_FILE}, outfile)

def build_prod_jscripts(outfile):
    replace_text_with_file_context({'product_jscript':PRODUCT_JSCRIPT_FILE}, outfile)

def build_google_anlytics(outfile):
    replace_text_with_file_context({'google_anlytics':GOOGLE_ANLYTICS_FILE}, outfile)

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
            copyfile(SUBPROD_W_SIDEMENU_TMPLT_FILE, tmp_side_file)
        else:
            copyfile(SUBPROD_TMPLT_FILE, tmp_side_file)
        for j in side_prods[key]:
            function_table[j]({j: side_prods[key][j]}, tmp_side_file)

        with open(tmp_side_file, 'r') as f:
            total_side_txt += f.read()

        total_side_txt += '\n'

        i += 1
        key = 'side_prod{}'.format(i)

    replace_text({'side_prods': total_side_txt}, outfile)

    return

def build_sideprod_menu(menu, nav_menuconf):
    with open(SIDEPROD_MENU_TMPLT_FILE, 'r') as fin:
        side_menu_text = fin.read()
    list_text = ''
    for i in nav_menuconf['menu']:
        if i.lower() == menu.lower():
            for j in nav_menuconf['menu'][i]:
                link = '/{}/{}/{}.html'.format(menu.lower(),
                                               j.lower(),
                                               j.lower())
                list_text += '''<li><a class="btn btn-default"''' \
                             '''href="{}">{}</a></li>\n'''.format(link, j)
            break

    side_menu_text = side_menu_text.replace(
            '###side_prod_menu###', list_text)
    side_menu_text = side_menu_text.replace(
            '###menu###', i)
    return side_menu_text


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
    parser.add_option("-i", "--prod_schema", dest="infile")
    parser.add_option("-n", "--navmenu_schema", dest="navmenufile")
    parser.add_option("-o", "--outfile", dest="outfile")
    (opt, args) = parser.parse_args()

    if not opt.infile or not opt.navmenufile:
        print "prod_schema and navmenu_schema are mandatory!!!"
        parser.print_help()
        return

    conf = yaml.load(open(opt.infile))
    nav_menu_conf = yaml.load(open(opt.navmenufile))

    if not opt.outfile:
        outfile = '{}/{}/{}/{}.html'.format(PROJ_ROOT,
                                            conf['hirarchy'].lower(),
                                            conf['product'].lower(),
                                            conf['product'].lower())

    copyfile(PROD_HTML_TMPLT_FILE, outfile)

    build_site_head(outfile)
    build_site_navigation(conf['hirarchy'], outfile)
    build_site_footer(outfile)
    build_prod_jscripts(outfile)
    #build_google_anlytics(outfile)

    for i in conf:
        if i in function_table:
            function_table[i]({i: conf[i]}, outfile)

    side_prod_menu_cont = build_sideprod_menu(conf['hirarchy'].lower(),
                                              nav_menu_conf)
    #side_prod_menu_contfile = '{}/contents/{}_side_prod.menu.content'.format(
    #                                        PROJ_ROOT, 
    #                                        conf['hirarchy'])
    #if os.path.exists(side_prod_menu_contfile):
    #    replace_text_with_file_context(
    #            {'side_prod_menu': side_prod_menu_contfile},
    #            outfile)
    #else:
    #    replace_text({'side_prod_menu': ''}, outfile)

    replace_text({'side_prod_menu': side_prod_menu_cont}, outfile)

    build_section_id_product(conf, outfile)

    print outfile + ' is generated'

if __name__ == "__main__":
        sys.exit(main())    # pylint: disable=E1120

