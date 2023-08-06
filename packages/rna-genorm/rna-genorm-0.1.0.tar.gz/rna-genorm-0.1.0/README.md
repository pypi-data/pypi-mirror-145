# geNorm
A Python package for RNAseq housekeeping (or, reference) normalisation.

[Read the docs](https://hylkedonker.gitlab.io/genorm).

You can:
- Run the geNorm algorithm [1], which automatically selects reference genes by recursively eliminating genes with high $`M`$
  value.
-  Compute the gene-stability measure $`M`$ for reference genes in a given set of samples.

Here, $`M`$ is defined in terms of the average variation in log-ratio expression:
```math
M_j = \sum_{k=1}^n\frac{V_{jk}}{n-1}
```
where
```math
A_{jk}^{(i)} = \log_2 \frac{a_{ij}}{a_{jk}}; V_{jk} = \sqrt{\mathrm{Var}(A_{jk})};
```
with expression $`a_{ij}`$ referring to gene $`j`$ in sample $`i`$.

## Installation
You can grab `geNorm` from the Python Package Index:
```bash
pip3 install rna-genorm
```


## Example
```python
from pandas import DataFrame
from genorm import m_measure, genorm


# Expression data for three control genes.
counts = DataFrame(
    [[ 1,  2,  1],
    [ 3,  6,  5],
    [ 5, 10,  9],
    [ 3,  6,  5]],
    columns=['gene_a', 'gene_b', 'gene_c'],
    index=[f'sample_{i}' for i in range(1, 5)],
)

# Compute `M` value for this set of control genes.
m_measure(counts)

# Select top 2 control genes with lowest `M`.
gene_names, m_values = genorm(counts, n_stop=2)
```

## Acknowledgements
Made by Hylke Donker & Bram van Es and open sourced under the [Apache 2 license](LICENSE).

# References:
[1]: Vandesompele, Jo, et al. "[Accurate normalization of real-time quantitative
RT-PCR data by geometric averaging of multiple internal control genes.](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2002-3-7-research0034)" Genome biology
3.7 (2002): 1-12.