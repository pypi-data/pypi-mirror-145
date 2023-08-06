import os
import time
import re
from . import util
from .data import DATA
from .block import BLOCK
from .tcf import TABINDEX, TCF, TCFMAP
from .conf import COLNAMES, COL_JUSTIFY
from rich.console import Console
from rich.table import Table
from rich.text import Text

class UKBSearch():
    opt = None
    runtime = {}
    out = ""
    rdatafilemap = {}

    def __init__(self, opt):
        self.opt = opt
        self.has_opt_error = False
        self.out = ""
        self.rdata_file_map = {}
        self.rdata_df_map = {}

    def run(self):
        self.opt['log'].info('COMMAND: ' + self.opt['cmd'])
        t0 = time.time()
        self.dispatch()
        t2 = time.time()

        self.opt['log'].info('Total running time: ' + str(round(t2-t0, 1))+' sec')
        self.opt['log'].info('END')


    def search(self):
        data = DATA()
        data.load_html_list(self.opt['path'])
        blocklist = data.search_description(self.opt['searchterm'], self.opt['logic'])
        if "console" in self.opt['outtype']:
            self.print_blocklist(blocklist, self.opt['searchterm'])
        if "udi" in self.opt['outtype']:
            self.print_udi(blocklist)
        if "csv" in self.opt['outtype']:
            self.save_csv_block(blocklist)
            self.opt['log'].info('SAVED SEARCH RESULT: ' + self.out)
        if len(self.opt['savedata']) > 0:
            self.save_data(blocklist)
    
    def save_data(self, blocklist):
        tcfmap = TCFMAP(self.opt['log'])
        for block in blocklist:
            if not block.fid in tcfmap.keys(): 
                tcfmap.add_tcf(block.fid, TCF(block.fid, self.opt['path'], self.opt['log']))
            tcfmap.tcfs[block.fid].add_udilist(block.get_listudi())
        tcfmap.save_data(self.opt['out'], self.opt['savedata'])
        
    def save_data_with_tcfmap(self, tcfmap):
        for outtype in self.opt['savedata']:
            outfile = tcfmap.get_outfilename(self.opt['out'], outtype)
            self.opt['log'].info("SAVING " + outtype + ", " + outfile + "  It takes a few minutes..")
            tcfmap.save_selected_udi(outfile, outtype)

        '''
        ##
        ## If you want to save files separately...
        ##
        for fid in tcfmap.keys():
            print("===>>>", fid)
            tcf = tcfmap[fid]
            if tcf.load_tcf():

                if "csv" in self.opt['savedata']:
                    outfile = tcf.get_outfilename(self.opt['out'], 'csv')
                    tcf.set_result_dataframe()
                    self.opt['log'].info("SAVING CSV.. " + outfile + "  It takes a few minutes..")
                    tcf.save_selected_udi_as_csv(outfile)
                
                if "csvi" in self.opt['savedata']:
                    outfile = tcf.get_outfilename(self.opt['out'], 'csv', '_inv')
                    self.opt['log'].info("SAVING CSV.. " + outfile + "  It takes a few minutes..")
                    tcf.save_selected_udi_as_csvi(outfile)

                if "rdata" in self.opt['savedata']:
                    outfile = tcf.get_outfilename(self.opt['out'], 'RData')
                    tcf.set_result_dataframe()
                    self.opt['log'].info("SAVING RDATA.. " + outfile + "  It takes a few minutes..")
                    tcf.save_selected_udi_as_rdata(outfile)
        '''
        


    def save_data_with_userinput_udilist(self):
        tcfmap = TCFMAP(self.opt['log'])
        tcfmap.set_userinput_udilist(self.opt['udilist'], self.opt['path'], self.opt['log'])
        self.opt['log'].info("SELECTED " + str(tcfmap.count_udi()) + " UDI(s) FROM " + str(len(tcfmap.tcfs.keys())) + " FILES.")
        tcfmap.save_data(self.opt['out'], self.opt['savedata'])

    def save_csv_block(self, blocklist):
        rst = []

        header = ["HTML"]
        header.extend(COLNAMES)
        header.append("File")
        rst.append(header)

        prev_3 = ""
        prev_4 = ""
        for block in blocklist:
            for row in block.get_listrows():
                if row[3] == "":
                    row[3] = prev_3
                    row[4] = prev_4
                else:
                    prev_3 = row[3]
                    prev_4 = row[4]
                rst.append([block.fid, row[0], row[1], row[2], row[3], row[4], block.htmlfile])

        self.out = util.check_ext(self.opt['out'], '.csv')
        util.save_csv(self.out, rst)

    def print_udi(self, blocklist):
        rst = []
        for block in blocklist:
            rst.append(block.fid)
            for row in block.get_listrows():
                rst.append(row[1])
        print()
        print (' '.join(rst))
        print()

    def print_blocklist(self, blocklist, terms=[]):
        console = Console()
        table = Table(show_header=True)
        table.add_column("HTML", justify="left")
        for k in range(len(COLNAMES)):
            table.add_column(COLNAMES[k], justify=COL_JUSTIFY[k])
        table.add_column("File", justify="left")

        patterns = util.get_patterns_from_terms(terms)
        pattern = r'|'.join(patterns)
        
        for block in blocklist:
            for row in block.get_listrows():
                if row[4] != "":
                    desc = Text()
                    arr_split = re.split(pattern, block.description, flags=re.IGNORECASE)
                    arr_findall = re.findall(pattern, block.description, flags=re.IGNORECASE)
                    for k in range(len(arr_split)):
                        desc.append(arr_split[k])
                        if k < len(arr_findall):
                            desc.append(arr_findall[k], style="bold magenta")
                    # desc.append(row[4])
                else:
                    desc = ""
                table.add_row(block.fid, row[0], row[1], row[2], row[3], desc, block.htmlfile)
        console.print(table)

    def dispatch(self):
        if len(self.opt['searchterm']) > 0:
            self.search()

        if len(self.opt['udilist']) > 0:
            self.save_data_with_userinput_udilist()

        if self.opt['index'] != "":
            tindex = TABINDEX(self.opt['index'], self.opt['log'])
            self.opt['log'].info('CALCULATING SIZE..')
            tindex.cal_size()
            self.opt['log'].info('START INDEXING..')
            tindex.transpose()
            tindex.index()
            self.opt['log'].info('GENERATED INDEX FILES: ' + tindex.tcfgz)