import os
from subprocess import check_call
from .utils import change_path,python_path
from DNBC4tools.__init__ import _root_dir

class Clean:
    def __init__(self, args):
        self.name = args.name
        self.outdir = args.outdir
        self.no_combine = args.no_combine

    def run(self):
        change_path()
        new_python = python_path()

        clean_cmd = ['%s %s/rna/clean_sample.py --outdir %s'%(new_python,_root_dir,self.outdir)]
        if self.name:
            clean_cmd += ['--name %s'%self.name]
        if self.no_combine:
            clean_cmd += ['--no_combine']
        clean_cmd = ' '.join(clean_cmd)
        print(clean_cmd)
        check_call(clean_cmd,shell=True)

def clean(args):
    Clean(args).run()

def parse_clean(parser):
    parser.add_argument('--name',help='sample name')
    parser.add_argument('--outdir',help='output dir, default is current directory', default=os.getcwd())
    parser.add_argument('--no_combine', action='store_true',help="Don't combine sample result.")

