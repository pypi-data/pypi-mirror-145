from typing import Union

from numpy import arange, argmax, delete, einsum, log2, ndarray, std, sum, unique
from pandas import DataFrame, Series


def _m_numpy(gene_expression: ndarray) -> ndarray:
    """Internal control gene-stability measure `M`.

    Computes Eq. (4) in Ref. [1].

    [1]: Vandesompele, Jo, et al. "Accurate normalization of real-time quantitative
    RT-PCR data by geometric averaging of multiple internal control genes." Genome
    biology 3.7 (2002): 1-12.
    """

    if not (gene_expression > 0).all():
        raise ValueError(
            'Expression domain error: not all expression data are strictly positive!'
            )

    a = gene_expression
    # Eq. (2): A_{jk}^{(i)} = log_2 (a_{ij} / a_{ik})
    A = log2(einsum('ij,ik->ijk', a, 1/a))
    # Eq. (3)
    V = std(A, axis=0)
    # Eq. (4) N.B., Since V_{j=k} is zero, we can simply ignore it since it does not
    # contribute to calculation.
    n = V.shape[1]
    return sum(V, axis=1) / (n-1)


def m_measure(gene_expression: Union[ndarray, DataFrame]) -> Union[ndarray, Series]:
    """Internal control gene-stability measure `M` as described in Ref. [1].

    [1]: Vandesompele, Jo, et al. "Accurate normalization of real-time quantitative
    RT-PCR data by geometric averaging of multiple internal control genes." Genome
    biology 3.7 (2002): 1-12.

    Args:
        gene_expression: Gene expression counts of `m` samples (rows) and `n` internal
            control genes (columns). Expression must be strictly positive.

    Raises:
        ValueError: Expression not strictly positive.
    """
    if isinstance(gene_expression, DataFrame):
        m_values = _m_numpy(gene_expression.to_numpy())
        return Series(m_values, index=gene_expression.columns)
    return _m_numpy(gene_expression)


def _genorm_numpy(gene_expression: ndarray, n_stop: int = 20, verbose: bool = False
) -> tuple[list, ndarray]:
    """Backward elimination of genes by M value.

    Returns:
        First element are the selected genes, and the second are the corresponding `M`
        values.

    Raises:
        ValueError: Expression not strictly positive, or `n_stop` equal or larger than
            number of genes (columns).
    """
    if not (gene_expression > 0).all():
        raise ValueError(
            'Expression domain error: not all expression data are strictly positive!'
            )
    elif gene_expression.shape[1] <= n_stop:
        raise ValueError('Nothing to select, since `n_stop` >= number of genes.')

    n_genes = gene_expression.shape[1]
    eliminated: list[int] = []
    for _ in range(n_genes - n_stop):
        # Index to map the index of `expression_subset` back to `gene_expression`.
        subset_index = delete(arange(n_genes), eliminated)
        expression_subset = delete(gene_expression, eliminated, axis=1)

        m_values = _m_numpy(expression_subset)
        idx: int = subset_index[argmax(m_values)]

        # Print . indicating progress.
        if verbose:
            print('.', end='')

        eliminated.append(idx)

    # Check that all eliminated values are unique.
    assert len(unique(eliminated)) == len(eliminated)

    final_subset = delete(gene_expression, eliminated, axis=1)
    selected = [i for i in range(n_genes) if i not in eliminated]

    # Print end of line.
    if verbose:
        print('')

    return selected, _m_numpy(final_subset)


def genorm(gene_expression: Union[ndarray, DataFrame], n_stop: int = 20, verbose: bool = False,
) -> tuple[list, Union[ndarray, Series]]:
    """geNorm performs recursive backward selection of genes with low `M`-value.

    Args:
        gene_expression: Gene expression counts of `m` samples (rows) and `n` internal
            control genes (columns). Expression must be strictly positive.
        n_stop: Stopping criterion: stop after selecting this many genes.

    Returns:
        First element are the selected genes, and the second are the corresponding `M`
        values.

    Raises:
        ValueError: Expression not strictly positive.
    """
    if isinstance(gene_expression, DataFrame):
        selected_idx, m_values = _genorm_numpy(gene_expression.to_numpy(), n_stop, verbose)
        selected_genes = gene_expression.columns[selected_idx]
        m_series = Series(m_values, index=selected_genes)
        return selected_genes.tolist(), m_series
    return _genorm_numpy(gene_expression, n_stop, verbose)