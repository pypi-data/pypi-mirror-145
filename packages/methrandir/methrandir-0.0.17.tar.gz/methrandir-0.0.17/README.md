# Mehtrandir

## Installation

This package is available on [anaconda](https://anaconda.org/skanderPoit/methrandir) and can be installer with the following command

```bash
conda install -c skanderpoit methrandir
```

## Usage
Directly from the command line:
```bash
usage: methrandir.py [-h] -f FILES [-o OUT_PREFIX] [-outdir OUTDIR] [-m METHOD] [-c MIN_COVERAGE] [-C CONTEXTS [CONTEXTS ...]] [-F FORCE] [-p P_VALUE]

Methylation Data Overview Utility

optional arguments:
  -h, --help            show this help message and exit
  -f FILES, --files FILES
                        tab seperated file containing paths of sorted bismark CX reports and their
  -o OUT_PREFIX, --out_prefix OUT_PREFIX
                        output files prefix
  -outdir OUTDIR, --outdir OUTDIR
                        output directory
  -m METHOD, --method METHOD
                        model biological replicates : weighted_average | anova
  -c MIN_COVERAGE, --min_coverage MIN_COVERAGE
                        minimum number of reads for each position on all samples
  -C CONTEXTS [CONTEXTS ...], --contexts CONTEXTS [CONTEXTS ...]
                        list of contexts to be considered for downstream analysis : CG,CHG,CHH
  -F FORCE, --force FORCE
                        Force recreation of filtered files
  -p P_VALUE, --p_value P_VALUE
                        p_value for statistical tests
```
Or imported as a module in your python scri

```python
from methrandir import methrandir
```
methrandir.readlines() needs a `.tsv` file describing raw data(Sorted Bismark CX reports) and can take other arguments to further filter data for each position.

methrandir.compute_pca() takes in the product of readfiles and applies pca and generates some graphs.