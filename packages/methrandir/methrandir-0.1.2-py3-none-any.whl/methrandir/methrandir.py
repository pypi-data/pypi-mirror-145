#!/home/shatira/miniconda3/bin/python
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
import numpy as np
import plotly.express as px
from itertools import zip_longest
import csv
from collections import Counter
import os
import itertools
from scipy.stats import f_oneway
import argparse
import matplotlib.pyplot as plt

def readfiles(files, outdir="methrandir_output", prefix="methrandir", coverage=4, method="weighted_average",force=False,p_value=0.05):
    outputfile = os.path.join(outdir, f"{prefix}.filtered_methylation.csv")
    if (not os.path.isfile(outputfile) or force):
        if not os.path.exists(outdir) and outdir != "":
            os.mkdir(outdir)
        units = pd.read_csv(files, sep='\t', header=0)
        combined = units['group']+'_'+units['replicate'].astype(str)
        design = units['group']
        mapdesign = list(Counter(design).values())

        with open(outputfile, 'w', newline="") as all:
            wr = csv.writer(all, quoting=csv.QUOTE_MINIMAL)
            if method == "weighted_average":
                wr.writerow((["chr", "position","context","tri_context"] + list(dict.fromkeys(design))))
            elif method == "raw" or method == "anova":
                wr.writerow(["chr", "position","context","tri_context"] + list(combined.values))
            fileList = units.loc[:, "path"].values
            files = [open(filename) for filename in fileList]
            for lines in zip_longest(*files, fillvalue=''):
                keep = []
                meths = []
                unmeths = []
                broken = False
                metaLine = lines[1].split('\t')
                meta = [el.strip('\n') for el in metaLine[0:2] + metaLine[5:7]]
                # meta = metaLine[0:2] + metaLine[5] + metaLine[-1:].rstrip('\n')
                # attempt to filter
                for line in lines:
                    line = line.split('\t')
                    meth = int(line[3])
                    unmeth = int(line[4])
                    if meth + unmeth < coverage:
                        broken = True
                        break
                    else:
                        meths.append(meth)
                        unmeths.append(unmeth)
                        keep.append(meth/sum([meth, unmeth]))
                if broken:
                    pass
                else:
                    weighted_avg = []
                    grouped = []
                    groupcov = []
                    counter = 0
                    cov = list(zip(meths, unmeths))
                    cov = [sum(x) for x in cov]
                    if method == "weighted_average":
                        for l in mapdesign:
                            grouped.append(keep[counter:l+counter])
                            groupcov.append(cov[counter:l+counter])
                            counter += l
                        for i in range(len(mapdesign)):
                            weighted_avg.append(np.average(
                                grouped[i], weights=groupcov[i]))
                        wr.writerow(meta + weighted_avg)
                    elif method == "raw":
                        wr.writerow(meta + keep)
                    elif method == "anova":
                        for l in mapdesign:
                            grouped.append(keep[counter:l+counter])
                            counter += l
                        stat, p = f_oneway(*grouped)
                        if p < p_value:
                            wr.writerow(meta + keep)   
            for fh in files:
                fh.close()

def compute_pca(files,file, outdir="methrandir_output", prefix="methrandir",contexts=["CG","CHG","CHH"],method="weighted_average"):
    all = pd.read_csv(file, sep=",", header=0)
    units = pd.read_csv(files, sep='\t', header=0)
    design = units['group']
    for context in contexts:
        df = all.loc[all["context"]== context].iloc[:,4:].T
        index = all.iloc[:, 4:].columns
        symbol = index if method == "weighted_average" else design
        pca = PCA(n_components=3)
        components = pca.fit_transform(df.values)
        print(components.shape)
        total_var = pca.explained_variance_ratio_.sum() * 100
        p = pca.explained_variance_ratio_
        labels={'0': f'PC 1 : {p[0]*100:.2f}%',
                    '1': f'PC 2 : {p[1]*100:.2f}%', '2': f'PC 3 : {p[2]*100:.2f}%'}
        fig = px.scatter_3d(
            components, x=0, y=1, z=2, color=index,
            title=f'Total Explained Variance: {total_var:.2f}%',
            labels=labels)
       
        fig.write_html(os.path.join(outdir, f"{prefix}.3DPCA-{context}.HTML"))
        
        fig = px.scatter(components,x=0, y=1, color=index,symbol=symbol,
                        labels={'0': f'PC 1 : {p[0]*100:.2f}%','1': f'PC 2 : {p[1]*100:.2f}%'})
    
        fig.write_html(os.path.join(outdir, f"{prefix}.2DPCA-{context}.HTML"))
        g = sns.clustermap(components,yticklabels=index,xticklabels=labels.values())
        plt.savefig(os.path.join(outdir,f"{prefix}.clustermap-{context}.png"))



    
    # work in progress.... Discrete Fourier Transform + cross correlation for similarity extraction
def main():
    parser = argparse.ArgumentParser(description='Methylation Data Overview Utility')
    parser.add_argument(
        "-f", "--files", help="tab seperated file containing paths of sorted bismark CX reports and their",required=True)
    parser.add_argument(
        "-o", "--out_prefix", help="output files prefix", default="methrandir")
    parser.add_argument(
        "-outdir", "--outdir", help="output directory", default="methrandir_output")
    parser.add_argument(
        "-m", "--method", type=str,help="model biological replicates : weighted_average | anova", default="weighted_average")
    parser.add_argument(
        "-c", "--min_coverage", type=int, help="minimum number of reads for each position on all samples", default=4)
    parser.add_argument(
        "-C", "--contexts",nargs ="+", help="list of contexts to be considered for downstream analysis : CG,CHG,CHH", default=["CG","CHG","CHH"])
    parser.add_argument(
        "-F", "--force", type=bool, help="Force recreation of filtered files", default=False)
    parser.add_argument(
        "-p", "--p_value", type=bool, help="p_value for statistical tests", default=0.05)
    args = parser.parse_args()
    print(args.contexts)
    
    readfiles(files=args.files, outdir=args.outdir,
            prefix=args.out_prefix, coverage=args.min_coverage, method=args.method,force=args.force,p_value=args.p_value)
    compute_pca(files=args.files,file=os.path.join(
        args.outdir, f"{args.out_prefix}.filtered_methylation.csv"), outdir=args.outdir,method=args.method, prefix=args.out_prefix,contexts=args.contexts)    
if __name__ == "__main__":
    main()
