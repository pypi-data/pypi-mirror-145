import os
from .utils import str_mkdir,logging_call,judgeFilexits,change_path
from DNBC4tools.__init__ import _root_dir

class Analysis:
    def __init__(self,args):
        self.name = args.name
        self.matrix = args.matrix
        self.qcdim = args.qcdim
        self.clusterdim = args.clusterdim
        self.doubletpercentage = args.doubletpercentage
        self.mitpercentage = args.mitpercentage
        self.mtgenes = args.mtgenes
        self.minfeatures = args.minfeatures
        self.PCusage = args.PCusage
        self.resolution = args.resolution
        self.species = args.species
        self.outdir = os.path.join(args.outdir,args.name)
    
    def run(self):
        judgeFilexits(self.matrix)
        str_mkdir('%s/03.analysis/QC'%self.outdir)
        str_mkdir('%s/03.analysis/Clustering'%self.outdir)
        str_mkdir('%s/log'%self.outdir)
        change_path()

        qc_cmd = 'Rscript %s/rna/QC_analysis.R -I %s -D %s -P %s -M %s -MP %s -F %s -B %s -O %s/03.analysis'\
            %(_root_dir,self.matrix,self.qcdim,self.doubletpercentage,self.mtgenes,self.mitpercentage,self.minfeatures,self.name,self.outdir)
        cluster_cmd = 'Rscript %s/rna/Cluster_analysis.R -I %s/03.analysis/QC -D %s -PC %s -RES %s -O %s/03.analysis -SP %s' \
            %(_root_dir,self.outdir,self.clusterdim,self.PCusage,self.resolution,self.outdir,self.species)
        logging_call(qc_cmd,'analysis',self.outdir)
        logging_call(cluster_cmd,'analysis',self.outdir)
        
def analysis(args):
    Analysis(args).run()

def parse_analysis(parser):
    parser.add_argument('--name',required=True,help='Sample name')
    parser.add_argument('--matrix',required=True,help='Count matrix dir,contain barcodes.tsv,features.tsv,matrix.mtx')
    parser.add_argument('--qcdim',type=int,default=20,help="DoubleFinder's PCs parameter, the number of significant principal components, default is 20.")
    parser.add_argument('--clusterdim',type=int,default=20,help='The principal components used for clustering, default is 20.')
    parser.add_argument('--doubletpercentage',type=float,default=0.05,help='Assuming doublet formation rate, tailor for your dataset, default is 0.05')
    parser.add_argument('--mitpercentage',type=int,default=5,help='Filter cells with mtgenes percentage, default is 5',)
    parser.add_argument('--mtgenes',default='False',help='set mitochondrial genes(mtgene list file path) or Homo or False, default is False')
    parser.add_argument('--minfeatures',type=int,default=200,help='Filter cells with minimum nfeatures, default is 200.',)
    parser.add_argument('--PCusage',type=int,default=50,help='The total number of principal components for PCA, default is 50')
    parser.add_argument('--resolution',type=float,default=0.5,help='Cluster resolution, default is 0.5',)
    parser.add_argument('--species',type=str,default='other',help='select species for cell annotation, only human and mouse can do auto annotation.')
    parser.add_argument('--outdir',help='output dir, default is current directory.',default=os.getcwd())
    return parser