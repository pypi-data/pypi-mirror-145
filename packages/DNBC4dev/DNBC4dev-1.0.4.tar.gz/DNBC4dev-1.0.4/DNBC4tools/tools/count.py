import os,subprocess
from .utils import str_mkdir,python_path,logging_call,rm_temp,judgeFilexits,change_path
from DNBC4tools.__init__ import _root_dir

class Count:
    def __init__(self,args):
        self.name = args.name
        self.bam = args.bam
        self.cDNAbarcodeCount = args.cDNAbarcodeCount
        self.Indexreads = args.Indexreads
        self.oligobarcodeCount = args.oligobarcodeCount
        self.thread = args.thread
        self.oligotype = args.oligotype
        self.outdir = os.path.join(args.outdir,args.name)
        self.expectNum = args.expectNum
    
    def run(self):
        judgeFilexits(self.bam,self.cDNAbarcodeCount,self.Indexreads,self.oligobarcodeCount,self.oligotype)
        str_mkdir('%s/02.count'%self.outdir)
        str_mkdir('%s/log'%self.outdir)
        change_path()
        new_python = python_path()
        cellCalling_cmd = [
            'Rscript %s/rna/cell_calling.R'%_root_dir,'-i',
            '%s/01.data/beads_stat.txt'%self.outdir,
            '-o %s/02.count/'%self.outdir]
        if self.expectNum:
            cellCalling_cmd += ['-f %s'%self.expectNum]
        cellCalling_cmd= ' '.join(cellCalling_cmd)
        mergeBarcodes_cmd = '%s/soft/mergeBarcodes -b %s/02.count/beads_barcode_all.txt -f %s -n %s -o %s/02.count/'\
            %(_root_dir,self.outdir,self.Indexreads,self.name,self.outdir)
        similiarBeads_cmd = '%s/soft/s1.get.similarityOfBeads -n %s %s %s/02.count/%s_CB_UB_count.txt %s/02.count/beads_barcodes.txt %s %s/02.count/Similarity.all.csv %s/02.count/Similarity.droplet.csv %s/02.count/Similarity.droplet.filtered.csv'\
            %(_root_dir,self.thread,self.name,self.outdir,self.name,self.outdir,self.oligotype,self.outdir,self.outdir,self.outdir)
        combineBeads_cmd = '%s %s/rna/combinedListOfBeads.py %s/02.count/Similarity.droplet.filtered.csv %s/02.count/%s_combined_list.txt'\
            %(new_python,_root_dir,self.outdir,self.outdir,self.name)
        CellMerge_cmd = '%s %s/rna/cellMerge.py --indir %s/02.count --name %s'\
            %(new_python,_root_dir,self.outdir,self.name)
        tagAdd_cmd = '%s/soft/tagAdd -n %s -bam %s -file %s/02.count/%s_barcodeTranslate_hex.txt -out %s/02.count/anno_decon.bam -tag_check CB:Z: -tag_add DB:Z: '\
            %(_root_dir,self.thread,self.bam,self.outdir,self.name,self.outdir)
        PISA_count_cmd = '%s/soft/PISA count -@ %s -tag DB -anno-tag GN -umi UB -outdir %s/02.count/matrix %s/02.count/anno_decon.bam'\
            %(_root_dir,self.thread,self.outdir,self.outdir)
        saturation_cmd = '%s/soft/GN_stat_modifymeanreads -bam %s/02.count/anno_decon.bam -barcode %s/02.count/%s_barcodeTranslate_hex.txt -name %s -outdir %s/02.count -@ %s'\
            %(_root_dir,self.outdir,self.outdir,self.name,self.name,self.outdir,self.thread)
        cellReport_cmd = 'Rscript %s/rna/cell_report.R -I %s/02.count/merge_cell.stat -M %s/02.count/matrix -S %s/02.count/%s_Saturation.tsv.gz -O %s/02.count'\
            %(_root_dir,self.outdir,self.outdir,self.outdir,self.name,self.outdir)

        logging_call(cellCalling_cmd,'count',self.outdir)
        subprocess.check_call("cat %s | awk '{print $1}'> %s/02.count/beads_barcode_all.txt"\
            %(self.cDNAbarcodeCount,self.outdir), shell=True)
        logging_call(mergeBarcodes_cmd,'count',self.outdir)
        logging_call(similiarBeads_cmd,'count',self.outdir)
        logging_call(combineBeads_cmd,'count',self.outdir)
        logging_call(CellMerge_cmd,'count',self.outdir)
        logging_call(tagAdd_cmd,'count',self.outdir)
        str_mkdir('%s/02.count/matrix'%self.outdir)
        logging_call(PISA_count_cmd,'count',self.outdir)
        logging_call(saturation_cmd,'count',self.outdir)
        logging_call(cellReport_cmd,'count',self.outdir)
        rm_temp('%s/02.count/%s_CB_UB_count.txt'%(self.outdir,self.name),'%s/02.count/beads_barcode_all.txt'%self.outdir)

def count(args):
    Count(args).run()

def parse_count(parser):
    parser.add_argument('--name',help='sample name')
    parser.add_argument('--bam',help='Bam file after star and anno, eg./01.data/final.bam')
    parser.add_argument('--cDNAbarcodeCount',help='Read count per cell barcode for cDNA, eg./01.data/cDNA_barcode_counts_raw.txt.',)
    parser.add_argument('--Indexreads',help='Barcode reads generate by scRNAparse, eg./01.data/Index_reads.fq.')
    parser.add_argument('--oligobarcodeCount',help='Read count per cell barcode for oligo, eg./01.data/Index_barcode_counts_raw.txt.')
    parser.add_argument('--oligotype',help='Whitelist for oligo, default is %s/config/oligo_type8.txt'%_root_dir,default='%s/config/oligo_type8.txt'%_root_dir)
    parser.add_argument('--thread',help='Analysis threads. default is 4.',type=int,default=4)
    parser.add_argument('--outdir',help='output dir, default is current directory.',default=os.getcwd())
    parser.add_argument('--expectNum',help='The number of beads intercepted by the inflection point')
    return parser