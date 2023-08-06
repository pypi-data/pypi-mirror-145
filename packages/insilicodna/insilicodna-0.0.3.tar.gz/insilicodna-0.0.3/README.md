# InSilicoDNA

**_Note: This package is still in a planning phase and is not intended for external usage_**

Why create synthetic molecular data when there is an ever-growing body of real data to use? Simply stated, control. For the Engineer or Data Engineer, it is critical to have data when building pipelines. For the Scientist, Data Scientist, or Machine Learning Engineer, it is critical to have data when modeling and testing assumptions. While there are now many sets of real molecular data to select from, there are few cases where _all_ types of data exist for a population of individuals in an unrestricted manner.

## Getting Started
### From CLI

Review options with `--help`
```
% insilicodna --help
```
Print common usage
```
% insilicodna
```
Create .fasta and .gff3 synthetic data for 50 genes
```
% insilicodna --gene-count 50 --fasta --gff3
```

### From `python`
```
import insilicodna

insilicodna.generate_contig(
	output_prefix="MySyntheticData",
	n_genes=50,
	fasta_file=True,
	gff3_file=True)
```
