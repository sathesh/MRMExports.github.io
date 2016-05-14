#!/usr/bin/env python
import sys
import yaml
from optparse import OptionParser
from shutil import copyfile
from buildfns_lib import *
from config import *

def build_menuitem(mitem, link, outfile):
    copyfile(NAV_MENU_DROPDN_ITEMS_TMPLT_FILE, outfile)
    replace_text({'menu_item': mitem}, outfile)
    replace_text({'menu_item_link': link}, outfile)
    
def build_mainmenu(menu, tmp_menu_file):
        mitem_text = ''
        for mitem in menus[menu]:
            tmp_mitem_file = '/tmp/tmp_mitem_file'
            link = '/{}/{}/{}.html'.format(menu.lower(), mitem.lower(), mitem.lower())
            build_menuitem(mitem, link, tmp_mitem_file)
            with open(tmp_mitem_file, 'r') as f:
                mitem_text += f.read()
 
def build_menus(conf, outfile):
    site_hdr = conf['site_header']
    menus = conf['menu']
    all_menu_text = ''
    for menu in menus:
        tmp_menu_file = '/tmp/tmp_menu_file'
        mitem_text = ''
        for mitem in menus[menu]:
            tmp_mitem_file = '/tmp/tmp_mitem_file'
            link = '/{}/{}/{}.html'.format(menu.lower(), mitem.lower(), mitem.lower())
            build_menuitem(mitem, link, tmp_mitem_file)
            with open(tmp_mitem_file, 'r') as f:
                mitem_text += f.read()

        copyfile(NAV_MENU_DROPDN_TMPLT_FILE, tmp_menu_file)
        replace_text({'menu_name': menu}, tmp_menu_file)
        replace_text({'menu_items': mitem_text}, tmp_menu_file)

        with open(tmp_menu_file, 'r') as f:
            all_menu_text += f.read()


    copyfile(NAV_TMPLT_FILE,outfile)
    replace_text({'main_menus': all_menu_text}, outfile)
    replace_text({'site_header': site_hdr}, outfile)
    


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

    outfile = opt.outfile
    if not outfile:
        outfile = SITE_NAVIGATION_FILE_GEN

    build_menus(conf, outfile)


    print outfile + ' is generated'

if __name__ == "__main__":
        sys.exit(main())    # pylint: disable=E1120

