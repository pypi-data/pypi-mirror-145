import os
from .utils import str_mkdir,judgeFilexits,start_print_cmd,change_path
from DNBC4tools.__init__ import _root_dir

class Runpipe:
    def __init__(self, args):
        self.name = args.name
        self.cDNAr1 = args.cDNAfastq1
        self.cDNAr2 = args.cDNAfastq2
        self.oligor1 = args.oligofastq1
        self.oligor2 = args.oligofastq2
        self.starIndexDir = args.starIndexDir
        self.gtf = args.gtf
        self.species = args.species
        
        self.outdir = args.outdir
        self.thread = args.thread
        self.cDNAconfig = args.cDNAconfig
        self.oligoconfig = args.oligoconfig
        self.oligotype = args.oligotype
        self.expectNum = args.expectNum
        
        self.process = args.process
        self.nosecondary = args.nosecondary
        self.include_introns = args.include_introns
        self.need_bam = args.need_bam
        self.mixseq = args.mixseq
        self.dry = args.dry
        
    def runpipe(self):
        change_path()
        judgeFilexits(self.cDNAr1,self.cDNAr2,self.oligor1,self.oligor2,self.cDNAconfig,self.oligoconfig,self.starIndexDir,self.gtf,self.oligotype)
        data_cmd = ['DNBC4tools data --cDNAfastq1 %s --cDNAfastq2 %s --oligofastq1 %s --oligofastq2 %s --thread %s --name %s --cDNAconfig %s --oligoconfig %s --outdir %s --starIndexDir %s --gtf %s'
        %(self.cDNAr1,self.cDNAr2,self.oligor1,self.oligor2,self.thread,self.name,self.cDNAconfig,self.oligoconfig,self.outdir,self.starIndexDir,self.gtf)]
        if self.mixseq:
            data_cmd += ['--mixseq']
        if self.include_introns:
            data_cmd += ['--include_introns']
        data_cmd = ' '.join(data_cmd)

        count_cmd = ['DNBC4tools count --name %s --bam %s/%s/01.data/final.bam --cDNAbarcodeCount %s/%s/01.data/cDNA_barcode_counts_raw.txt --Indexreads %s/%s/01.data/Index_reads.fq --oligobarcodeCount %s/%s/01.data/Index_barcode_counts_raw.txt --thread %s --oligotype %s --outdir %s'
        %(self.name,self.outdir,self.name,self.outdir,self.name,self.outdir,self.name,self.outdir,self.name,self.thread,self.oligotype,self.outdir)]
        if self.expectNum:
            count_cmd += ['--expectNum %s'%self.expectNum]
        count_cmd = ' '.join(count_cmd)

        analysis_cmd = 'DNBC4tools analysis --name %s --matrix %s/%s/02.count/matrix --species %s --outdir %s'\
            %(self.name,self.outdir,self.name,self.species,self.outdir)
        
        report_cmd = ['DNBC4tools report --name %s --species %s --outdir %s'
        %(self.name,self.species,self.outdir)]
        if self.need_bam:
            report_cmd += ['--need_bam']
        report_cmd = ' '.join(report_cmd)

        if self.nosecondary:
            cmdlist = [data_cmd,count_cmd]
            if not self.dry:
                str_mkdir('%s'%os.path.join(self.outdir,self.name))
                start_print_cmd(data_cmd)
                start_print_cmd(count_cmd)
            else:
                shelllist = open('%s/%s.shell'%(self.outdir,self.name),'w')
                shelllist.write(data_cmd+'\n')
                shelllist.write(count_cmd+'\n')
                shelllist.close()
        else:
            pipelist = str(self.process).split(',')
            cmdlist = []
            if 'data' in pipelist:
                cmdlist.append(data_cmd)
            if 'count' in pipelist:
                cmdlist.append(count_cmd)
            if 'analysis' in pipelist:
                cmdlist.append(analysis_cmd)
            if 'report' in pipelist:
                cmdlist.append(report_cmd)
            if not self.dry:
                str_mkdir('%s'%os.path.join(self.outdir,self.name))
                for pipecmd in cmdlist:
                    start_print_cmd(pipecmd)
            else:
                shelllist = open('%s/%s.shell'%(self.outdir,self.name),'w')
                for pipecmd in cmdlist:
                    shelllist.write(pipecmd+'\n')
                shelllist.close()
            

    
def run(args):
    Runpipe(args).runpipe()

def parse_run(parser):
    parser.add_argument('--name', metavar='NAME',help='sample name', type=str)
    parser.add_argument('--cDNAfastq1', metavar='FASTQ',help='cDNA R1 fastq file, Multiple files are separated by comma, example A1_cDNA_R1.gz,A2_cDNA_R1.gz.', required=True)
    parser.add_argument('--cDNAfastq2', metavar='FASTQ',help='cDNA R2 fastq file, Multiple files are separated by comma, example A1_cDNA_R2.gz,A2_cDNA_R2.gz', required=True)
    parser.add_argument('--oligofastq1', metavar='FASTQ',help='oligo R1 fastq file, Multiple files are separated by comma, example A1_oligo_R1.gz,A2_oligo_R1.gz.',required=True)
    parser.add_argument('--oligofastq2', metavar='FASTQ',help='oligo R2 fastq file, Multiple files are separated by comma, example A1_oligo_R2.gz,A2_oligo_R2.gz.',required=True)
    parser.add_argument('--starIndexDir',type=str, metavar='PATH',help='Star index dir path.',required=True)
    parser.add_argument('--gtf',type=str, metavar='GTF',help='GTF file.')
    parser.add_argument('--species',type=str, metavar='STR',default='NA',help='Species name, example Human,Mouse and so on.Only Human,Mouse can analysis cell annotation. Default is NA')
    parser.add_argument('--outdir', metavar='PATH',help='output dir, default is current directory.', default=os.getcwd())
    parser.add_argument('--thread',type=int, metavar='INT',default=4,help='Analysis threads, defult is 4.')
    parser.add_argument('--cDNAconfig', metavar='JASON',help='whitelist file in JSON format for cDNA fastq, the value of cell barcode is an array in the JSON, defalut is %s/config/DNBelabC4_scRNA_beads_readStructure.json'%_root_dir,default='%s/config/DNBelabC4_scRNA_beads_readStructure.json'%_root_dir)
    parser.add_argument('--oligoconfig', metavar='JASON',help='whitelist file in JSON format for oligo fastq, the value of oligo barcode is an array in the JSON, defalut is %s/config/DNBelabC4_scRNA_oligo_readStructure.json'%_root_dir,default='%s/config/DNBelabC4_scRNA_oligo_readStructure.json'%_root_dir)
    parser.add_argument('--oligotype', metavar='FILE',help='Whitelist of oligo, default is %s/config/oligo_type8.txt'%_root_dir,default='%s/config/oligo_type8.txt'%_root_dir)
    parser.add_argument('--expectNum', metavar='INT',type=int, help='The number of beads intercepted by the inflection point, you are not satisfied with the number of cells in the result report, then decide whether to define this parameter or not.')
    parser.add_argument('--process', metavar='TEXT',help='Custom your analysis steps, steps are separated by comma, default is all step, include data,count,analysis,report.',type=str,default='data,count,analysis,report')
    parser.add_argument('--nosecondary',action='store_true',help='Disable secondary analysis, include data,count.')
    parser.add_argument('--include_introns', action='store_true',help='Include intronic reads in count.')
    parser.add_argument('--mixseq', action='store_true',help='cDNA and oligo sequence in same chip.')
    parser.add_argument('--need_bam', action='store_true',help='Generate a bam file in output dir.')
    parser.add_argument('--dry', help=' Do not execute the pipeline. Generate a pipeline shell file.',action='store_true')
    return parser
      