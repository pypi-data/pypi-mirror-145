import os
from .utils import rm_temp, str_mkdir,start_print_cmd,judgeFilexits,change_path,python_path
from DNBC4tools.__init__ import _root_dir

class Data:
    def __init__(self, args):
        self.cDNAr1 = args.cDNAfastq1
        self.cDNAr2 = args.cDNAfastq2
        self.oligor1 = args.oligofastq1
        self.oligor2 = args.oligofastq2
        self.thread = args.thread
        self.name = args.name
        self.cDNAconfig = args.cDNAconfig
        self.oligoconfig = args.oligoconfig
        self.outdir = os.path.join(args.outdir,args.name)
        self.starindex = args.starIndexDir
        self.gtf = args.gtf
        self.include_introns = args.include_introns
        self.mixseq = args.mixseq

    def run(self):
        judgeFilexits(self.cDNAr1,self.cDNAr2,self.oligor1,self.oligor2,self.cDNAconfig,self.oligoconfig,self.starindex,self.gtf)
        str_mkdir('%s/01.data'%self.outdir)
        str_mkdir('%s/log'%self.outdir)
        change_path()
        new_python = python_path()

        scRNA_parse_cmd = ['%s %s/rna/star_anno.py --name %s --cDNAfastq1 %s --cDNAfastq2 %s --oligofastq1 %s --oligofastq2 %s --thread %s --cDNAconfig %s --oligoconfig %s --outdir %s --starIndexDir %s --gtf %s'\
            %(new_python,_root_dir,self.name,self.cDNAr1,self.cDNAr2,self.oligor1,self.oligor2,self.thread,self.cDNAconfig,self.oligoconfig,self.outdir,self.starindex,self.gtf)]
        if self.include_introns:
            scRNA_parse_cmd += ['--include_introns']
        if self.mixseq:
            scRNA_parse_cmd += ['--mixseq']
        scRNA_parse_cmd = ' '.join(scRNA_parse_cmd)
        start_print_cmd(scRNA_parse_cmd)
        rm_temp('%s/01.data/Aligned.out.bam'%self.outdir)


def data(args):
    Data(args).run()

def parse_data(parser):
    parser.add_argument('--name',help='sample name', type=str)
    parser.add_argument('--outdir',help='output dir, default is current directory', default=os.getcwd())
    parser.add_argument('--cDNAfastq1',help='cDNAR1 fastq file, Multiple files are separated by comma.', required=True)
    parser.add_argument('--cDNAfastq2',help='cDNAR2 fastq file, Multiple files are separated by comma.', required=True)
    parser.add_argument('--cDNAconfig',help='whitelist file in JSON format for cDNA fastq,The value of cell barcode is an array in the JSON, consist of one or more segments in one or both reads.',default='%s/config/DNBelabC4_scRNA_beads_readStructure.json'%_root_dir)
    parser.add_argument('--oligofastq1',help='oligoR1 fastq file, Multiple files are separated by comma.',required=True)
    parser.add_argument('--oligofastq2',help='oligoR2 fastq file, Multiple files are separated by comma.',required=True)
    parser.add_argument('--oligoconfig',help='whitelist file in JSON format for oligo fastq',default='%s/config/DNBelabC4_scRNA_oligo_readStructure.json'%_root_dir)
    parser.add_argument('--thread',type=int, default=4,help='Analysis threads.')
    parser.add_argument('--starIndexDir',type=str, help='star index dir')
    parser.add_argument('--gtf',type=str, help='gtf file')
    parser.add_argument('--mixseq',action='store_true',help='cDNA and oligo sequence in same chip.')
    parser.add_argument('--include_introns', action='store_true',help='Include intronic reads in count.')
    return parser
