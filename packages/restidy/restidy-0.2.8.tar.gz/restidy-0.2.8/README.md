restidy
===
![PYPI](https://img.shields.io/pypi/v/restidy)

## Introduction

Restidy is write to process and tidy the AMR results after using ResFinder4.0

You will get the following results after using ResFinder4.0.
```
Sample01
├── PointFinder_prediction.txt
├── PointFinder_results.txt
├── PointFinder_table.txt
├── ResFinder_Hit_in_genome_seq.fsa
├── ResFinder_Resistance_gene_seq.fsa
├── ResFinder_results.txt
├── ResFinder_results_tab.txt
├── ResFinder_results_table.txt
├── pheno_table.txt
├── pheno_table_salmonella.txt
├── pointfinder_blast
```

Here are the content in ResFinder_results_tab.txt and PointFinder_results.txt files, which were mainly used as input data by restidy.

ResFinder_results_tab.txt
|Resistance gene | Identity | Alignment Length/Gene Length | Coverage | Position in reference | Contig | Position in contig | Phenotype | Accession no.|
|--- | --- | --- | --- | --- | --- | --- | --- | ---|
|aac(6')-Iaa  |   99.32  | 438/438 | 100.0 | 1..438 | contig1_denovo_ah19S2 | 164272..164709 | Aminoglycoside resistance | NC_003197 |
|qnrS1   | 100.00  | 657/657 |100.0 |  1..657 | contig26_denovo_ah19S2 | 7634..8290 | Quinolone resistance | AB187515 |


PointFinder_results.txt
|Mutation | Nucleotide change | Amino acid change | Resistance | PMID |
|---|---|---|---|---|
|parC p.T57S | ACC -> AGC | T -> S | Nalidixic acid,Ciprofloxacin | 15388468|


After using restidy, you will get the following results:
```
output
├── drug_pivot.csv # Pivot table of AMR corresponding drugs
├── pattern_process.csv # AMR and Drugs profile pattern
├── point_sum.csv # The summary of PointFinder result in pivot style
├── resfinder_sum.csv # The summary of ResFinder result in pivot style
└── resistance_statistic.csv # The number of isolates resistance to found drugs.
```

## Installation
Using pip:
```
pip3 install restidy==0.2.6
```

You could run the following command to run a test to check if restidy have been correctly installed.
```
restidy -i PATH_TO/demo_data -o OUTPUT_DIR
```


## Usage
```
restidy -i < resfinder4.0_result_directory > -o < output_file_directory >

Author: Qingpo Cui(SZQ Lab, China Agricultural University)
Version=0.2.6

optional arguments:
  -h, --help  show this help message and exit
  -i I        <input_path>: resfinder_result_path
  -o O        <output_file_path>: output_file_path
  -p P        True of False to process point mutation results
```
