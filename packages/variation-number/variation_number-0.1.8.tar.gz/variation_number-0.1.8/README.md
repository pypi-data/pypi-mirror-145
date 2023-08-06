# variation_number

A package for calculating the variation number of nucleotide/protein sequence using sequence orthologs.

This package can be found on [GitHub](https://github.com/jiaying2508/variation_number).

### Features

- Download orthologs
- Build phylogenetic trees
- Generate variation numbers

### Usage

```
import variation_number as vn
import os
gene = 'BRCA1'
seqtype =' protein'
outputDir = '{}/output'.format(os.getcwd())

# Download orthologs from NCBI orthologs database
acc = vn.getFasta(gene, outputDir, seqtype, refseqID=None, email='')

# Calculate variation numbers
vn.processVN(gene, outputDir, acc, seqtype)
```
