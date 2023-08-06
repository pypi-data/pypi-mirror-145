import plotly.express as px
import pandas as pd
import plotly as py
from plotly.graph_objs import Scatter, Layout, Data, Scattergl
import pandas as pd
import plotly.graph_objs as go
from plotly.io import *
import os
import argparse
import numpy as np
import sys
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline

print('''############################
# 1.barcode plot
############################''')
import plotly as py
from plotly.graph_objs import Scatter, Layout, Data, Scattergl
import pandas as pd
import plotly.graph_objs as go
from plotly.io import *
import os
import argparse
import numpy as np
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--outPath', type=str, help=
	'''input the outpath''',)
    parser.add_argument('--sample', type=str, help=
	'''input the samplename''',)
    args = parser.parse_args()
    return args.outPath,args.sample
    
outpath,samplename = get_args()

os.system('mkdir -p %s' % (outpath+"/04.report/div"))
os.system('mkdir -p %s' % (outpath+"/04.report/base64"))
os.system('mkdir -p %s' % (outpath+"/04.report/table"))
#os.system('mkdir -p %s' % (outpath+"/04.report/html"))

config = {
    'modeBarButtonsToRemove': ["autoScale2d","hoverClosestCartesian", "hoverCompareCartesian", "lasso2d",
    "zoomIn2d", "zoomOut2d", "sendDataToCloud",
    "toggleSpikelines" ,"logo"],
    'displaylogo': False,}
def plot_jaccard_knee_frag():
    #outpath = get_args()
    df = pd.read_csv(open(outpath+"/02.count/cutoff.csv"),encoding="utf-8",na_filter=False) 
    dp_first = set(df[df[["UMI"]].duplicated(keep="first")].index)
    dp_last = set(df[df[["UMI"]].duplicated(keep="last")].index)
    dp_inter = dp_first & dp_last
    df=df.drop(list(dp_inter),axis=0)
    df_True = df[(df['Beads'] == "true")]
    df_False = df[(df['Beads'] == "noise")]
    df_NA = df[(df['Beads'] == "NA")]
    trace0_x = list(df_True['barcodes'])
    trace0_y = list(df_True['UMI'])  
    trace1_x = list(df_False['barcodes'])
    trace1_y = list(df_False['UMI'])
    trace2_x = list(df_NA['barcodes'])
    trace2_y = list(df_NA['UMI'])
    blue_line = list(zip(trace0_x, trace0_y))
    blue_line = [list(i) for i in blue_line]
    red_line = list(zip(trace1_x, trace1_y))
    red_line = [list(i) for i in red_line]  
    gray_line = list(zip(trace2_x, trace2_y))
    gray_line = [list(i) for i in gray_line]
    trace0 = Scattergl(
        x = trace0_x,
        y = trace0_y,
        mode="lines",
        name="TRUE",
        line=dict(color="#005BAC",width=3) #zi #67267A
    )
    trace1 = Scattergl(
        x = trace1_x,
        y = trace1_y,
        mode="lines",
        name="NOISE",
        line=dict(color="gray",width=3)  
    )
    trace2 = Scattergl(
        x = trace2_x,
        y = trace2_y,
        mode="lines",
        name="NA",
        line=dict(color="gray",width=3)
        
    )
    config={
    'modeBarButtonsToRemove': ["autoScale2d","hoverClosestCartesian", "hoverCompareCartesian", "lasso2d",
    "zoomIn2d", "zoomOut2d", "sendDataToCloud",
    "toggleSpikelines" ,"logo"],
    'displaylogo': False,}
    data = [trace0, trace1, trace2]
    layout = Layout(
                        xaxis=dict(type="log", 
                        gridcolor="lightgrey",
                        title="Barcode in Rank-descending Order",
                        color="black",
                        showline=True,
                        zeroline=True,
                        linewidth=1,fixedrange= True,
                        linecolor="black"
                        ),
                        
                        yaxis = dict(
                        type="log",
                        title="Reads per Barcode",
                        gridcolor="lightgrey",
                        linewidth=1,fixedrange= True,
                        color="black",
                        linecolor="black"
                        ),
                        height=360,width=450,
                        plot_bgcolor='rgba(0,0,0,0)',
                        
                        hovermode='closest',
                        paper_bgcolor='white',
                        
                        legend=dict(
                        x=1,
                        y=1,
                        traceorder="normal",
                        font=dict(
                        family="Arial",
                        size=12,
                        color="black"
                        ),
                        bordercolor="Black",
                        borderwidth=0
                        ),
                        margin=dict(
                        l=0,
                        r=0,
                        b=0,
                        t=0,
                        pad=1
                        ),
                        font=dict(size=10)
    ) 
    fig = dict(data=data, layout=layout)
    py.offline.plot(fig, filename = outpath+"/04.report/div/barcode_rank.html",auto_open=False,config=config)
    fig2=py.offline.plot(fig, include_plotlyjs=False,show_link=False,output_type='div',config=config)
    fw = open(outpath+"/04.report/div/barcode_rank.div",'w')
    fw.write(fig2)

#path = get_args()
plot_jaccard_knee_frag()

print('''############################
# 2.cluster plot
############################''')
outdir=outpath
cluster_file = outdir+'/03.analysis/Clustering/cluster.csv'
cluster = pd.read_csv(cluster_file)
df = pd.read_csv(cluster_file)
df = df.sort_values(by='Cluster')
df[['Cluster']] = df[['Cluster']].astype('str')    
fig = px.scatter(df, x=df.UMAP_1, y=df.UMAP_2, color= df['Cluster'])

config=config
fig.update_layout(
    autosize=False,
    width=565,
    height=500,
    legend_title=dict(font=dict(size=16),text='Cluster',),
    legend=dict(font=dict(size=10,family='Arial'),),
    #paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(gridcolor='lightgray',),
    yaxis=dict(gridcolor='lightgray',)

    )
fig.update_traces(marker={'size': 3})
fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='gray')
fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='gray')
py.offline.plot(fig, filename = outdir+"/04.report/div/cluster.html",auto_open=False,config=config)
fig2=py.offline.plot(fig, include_plotlyjs=False,show_link=False,output_type='div',config=config)
fw = open(outdir+"/04.report/div/cluster.div",'w')
fw.write(fig2)
fw.close()
barplot_chsize = open(outdir+"/04.report/div/cluster.div","r").read()
barplot_chsize=barplot_chsize.replace('width:100%','width:565px')
fw1 = open(outdir+"/04.report/div/cluster_chsize.div","w")
fw1.write(barplot_chsize)
fw1.close()

####################plot nUMI
fig = px.scatter(df, x=df.UMAP_1, y=df.UMAP_2, color= df['nUMI'], )
config=config
fig.update_layout(
    autosize=False,
    width=520,
    height=500,
    legend_title=dict(font=dict(size=20),text='nUMI',),
    legend=dict(font=dict(size=20,family='Arial'),),
    #paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(gridcolor='lightgray',),
    yaxis=dict(gridcolor='lightgray',)
    )
fig.update_traces(marker={'size': 3})
fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='gray')
fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='gray')
py.offline.plot(fig, filename = outdir+"/04.report/div/cluster_nUMI.html",auto_open=False,config=config)
fig2=py.offline.plot(fig, include_plotlyjs=False,show_link=False,output_type='div',config=config)
fw = open(outdir+"/04.report/div/nUMI.div",'w')
fw.write(fig2)
fw.close()
barplot_chsize = open(outdir+"/04.report/div/nUMI.div","r").read()
barplot_chsize=barplot_chsize.replace('width:100%','width:480px')
fw1 = open(outdir+"/04.report/div/nUMI_chsize.div","w")
fw1.write(barplot_chsize)
fw1.close()
print('''###########################
# 2.2 cluster annotation plot
###########################''')
####################plot nUMI
if 'Predicted cell type' in df.columns:
    fig = px.scatter(df, x=df.UMAP_1, y=df.UMAP_2, color= df['Predicted cell type'], )
    config=config
    fig.update_layout(
    autosize=False,
    width=900,
    height=500,
    legend_title=dict(font=dict(size=16),text='Predicted cell type: cell number',),
    legend=dict(x=1.2,y=0.5,font=dict(size=10,family='Arial'),),
    #paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(gridcolor='lightgray',),
    yaxis=dict(gridcolor='lightgray',)
    )
    fig.update_traces(marker={'size': 3})
    fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='gray')
    fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='gray')
    py.offline.plot(fig, filename = outdir+"/04.report/div/anno.html",auto_open=False,config=config)
    fig2=py.offline.plot(fig, include_plotlyjs=False,show_link=False,output_type='div',config=config)
    fw = open(outdir+"/04.report/div/anno.div",'w')
    fw.write(fig2)
    fw.close()
    barplot_chsize = open(outdir+"/04.report/div/anno.div","r").read()
    barplot_chsize=barplot_chsize.replace('width:100%','width:565px')
    fw1 = open(outdir+"/04.report/div/anno_chsize.div","w")
    fw1.write(barplot_chsize)
    fw1.close()
print('''###########################
# 2.3 saturation plot
###########################''')
####################plot nUMI
outdir=outpath
saturation_file = outdir+'/02.count/'+samplename+'_Saturation.tsv.gz'
#saturation = pd.read_csv(saturation_file, sep="\t")
df = pd.read_csv(saturation_file, sep="\t",compression='gzip')

x=df['MeanReadsPerCell']
y=df['SaturationRatio']
xnew = np.linspace(x.min(),x.max(),300)
#ynew = make_interp_spline(x,y)(xnew)

import statsmodels.api as sm
lowess = sm.nonparametric.lowess
ynew = lowess(y, x, frac=0.27)
fig = px.line(df, x=ynew[:,0], y=ynew[:,1])

config=config
fig.update_layout(
    autosize=False,
    width=565,
    height=500,
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(gridcolor='lightgray',title="Mean Reads per Cell"),
    yaxis=dict(gridcolor='lightgray',title="Sequencing Saturation"),
    yaxis_range=[0,1]
    )
fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='gray')
fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='gray')
py.offline.plot(fig, filename = outdir+"/04.report/div/saturation.html",auto_open=False,config=config)
fig2=py.offline.plot(fig, include_plotlyjs=False,show_link=False,output_type='div',config=config)
fw = open(outdir+"/04.report/div/saturation.div",'w')
fw.write(fig2)
fw.close()

x=df['MeanReadsPerCell']
y=df['MedianGeneNumPerCell']
xnew = np.linspace(x.min(),x.max(),400)
#ynew = make_interp_spline(x,y)(xnew)
#fig = px.line(df, x=xnew, y=ynew )
ynew = lowess(y, x, frac=0.27)
fig = px.line(df, x=ynew[:,0], y=ynew[:,1])
config=config
fig.update_layout(
    autosize=False,
    width=520,
    height=500,
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(gridcolor='lightgray',title="Mean Reads per Cell"),
    yaxis=dict(gridcolor='lightgray',title="Median Genes per Cell")
    )
fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='gray')
fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='gray')
py.offline.plot(fig, filename = outdir+"/04.report/div/saturation2.html",auto_open=False,config=config)
fig2=py.offline.plot(fig, include_plotlyjs=False,show_link=False,output_type='div',config=config)
fw = open(outdir+"/04.report/div/saturation2.div",'w')
fw.write(fig2)
fw.close()

print('''###########################
# 3.png to base64
###########################''')
import base64
def png_to_base64(file=str(),filename=str()):    
    #inpath = get_args() 
    outpath = outdir + "/04.report"
    file_path = outdir+"/"+file
    base64_path = outpath+'/base64'+'/'+filename+'.base64'
    if os.path.isfile(file_path):
        with open(file_path, "rb") as f:
            base64_data = base64.b64encode(f.read())
            s = base64_data.decode()
            base64_path_f = open(base64_path, 'w')
            base64_path_f.write('<img src=data:image/'+'png'+';base64,'+s+">")
            base64_path_f.close()           
pictures = {'02.count/cellNumber_merge.png':'6','03.analysis/QC/raw_QCplot.png':'7'}
for k,v in pictures.items():
    png_to_base64(k,v) 

print('''###########################
# 4.csv to data-table
###########################''')
if os.path.exists(outdir+'/03.analysis/Clustering/marker.csv'): 
    df1= pd.read_csv(open(outdir+'/03.analysis/Clustering/marker.csv'),encoding="utf-8",dtype=str,)
    fw = open(outdir+'/04.report/table/marker-table.txt','w')
    for index, row in df1.iterrows():
        fw.write('<tr><td>'+row['Unnamed: 0']+'</td>'\
                +'<td>'+row['cluster']+'</td>'\
                +'<td>'+row['p_val_adj']+'</td>'\
                +'<td>'+row['p_val']+'</td>'\
                +'<td>'+row['avg_log2FC']+'</td>'\
                +'<td>'+row['pct.1']+'</td>'\
                +'<td>'+row['pct.2']+'</td>'\
            )
