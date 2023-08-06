
import argparse
import sys
import os
from . import util
import textwrap


def loading_config(opt):
    for line in open(opt['conf']):
        line = line.strip()
        if len(line) > 0 and line[0] != "#":
            arr = line.split("=")
            k1 = arr[0].strip().lower()
            v1 = arr[1].strip()
            if len(k1) > 0:
                opt[k1] = v1
    return opt
    

def print_option(opt):
    global NOPRINTOPTLIST
    # print("=======option=======")
    # for k1 in sorted(opt.keys()):
    #     if k1 not in NOPRINTOPTLIST:
    #         if k1 == "poslist" and len(opt[k1]) >= 4:
    #             print('-' + k1 + " : " + str(len(opt[k1])) + " variants")
    #         else:
    #             print('-' + k1 + " : " + str(opt[k1]))
    # print("====================")
    pass


def convert_valuetype(typestr):
    rsttype = None
    if typestr is not None:
        if typestr == "int":
            rsttype = int
        if typestr == "float":
            rsttype = float
    return rsttype


def get_options():
    global OPT
    # OPT = util.load_json(util.getDataPath('conf.json'))

    parser = argparse.ArgumentParser(usage='%(prog)s <sub-command> [options]',
                                    description='%(prog)s ver' + OPT['VERSION'] + " (" + OPT['VERSION_DATE'] + ")" + ': UKB HTML searcher')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ver' + OPT['VERSION'] + " (" + OPT['VERSION_DATE'] + ")")

    for a1 in OPT['options']:
        # valuetype = convert_valuetype(a1['type'])
        valuetype = a1['type']
        if a1['action'] is not None:
            parser.add_argument('-' + a1['param_a'], '--' + a1['param'], default=a1['default'], help=a1['help'], action=a1['action'])
        else:
            parser.add_argument('-' + a1['param_a'], '--' + a1['param'], default=a1['default'],
                                help=textwrap.dedent(a1['help']), nargs=a1['nargs'], type=valuetype)

    # parser.add_argument('-silence', dest='silence', action="store_true", default=False, help='don\'t print any log.')

    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1][0] != '-'):
        sys.argv.append('-h')
    opt = vars(parser.parse_args())

    if 'conf' in opt.keys() and opt['conf'] is not None and util.is_exist(opt['conf']):
        opt = loading_config(opt)

    opt['cmd'] = " ".join(sys.argv)
    

    return opt


### OPTION ####
OPT = {
  "TITLE": "UKBSearch",
  "VERSION": "0.2.2",
  "VERSION_DATE": "2022-04-05",
  "PROG": "ukbsearch",
  "options": [
    { "param_a": "s", "param": "searchterm", "default": [], "nargs": "*", "action": None, "choices": None, "type": None, "help": "search terms (ex: age gender)" },
    { "param_a": "l", "param": "logic", "default": "or", "nargs": None, "action": None, "choices": ["or","and"], "type": None, "help": "logical operator for multiple terms [or, and]" },
    { "param_a": "o", "param": "out", "default": None, "nargs": None, "action": None, "choices": None, "type": None, "help": "title of output file" },
    { "param_a": "t", "param": "outtype", "default": ["console"], "nargs": "*", "action": None, "choices": ["console","csv", "udi"], "type": None, "help": "output type [console, csv, udi]" },
    { "param_a": "p", "param": "path", "default": "/data2/UKbiobank/ukb_phenotype", "nargs": None, "action": None, "choices": None, "type": None, "help": "data file (.html, .Rdata) path (default: ./)" },
    { "param_a": "u", "param": "udilist", "default": [], "nargs": "*", "action": None, "choices": None, "type": None, "help": "UDI list (ex. ukb39003 3536-0.0 3536-1.0 3536-2.0"},
    { "param_a": "d", "param": "savedata", "default": [], "nargs": "*", "action": None, "choices": ["csv", "rdata"], "type": None, "help": "save data from tcf.gz [csv, rdata]" },
    { "param_a": "i", "param": "index", "default": "", "nargs": None, "action": None, "choices": None, "type": None, "help": "index tab file (ex. ukb39003.tab)" },
  ]
}
