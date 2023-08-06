from unittest import TestCase

from numpy import array, log2, ones, stack
from numpy.testing import assert_almost_equal, assert_array_equal
from pandas import DataFrame

from genorm.algorithms import genorm, _genorm_numpy, m_measure, _m_numpy


class TestgeNorm(TestCase):
    """Test M value computation and geNorm algorithm."""
    def setUp(self):
        """Construct artificial matrix with counts."""
        # Mean 3, variance 2.
        gene_a = array([1, 3, 5, 3])
        # Mean 6, variance 8.
        gene_b = gene_a * 2
        # Mean 5, variance 8.
        gene_c = gene_b - 1
        # A matrix of shape: 4x3.
        self.gene_expression = stack([gene_a, gene_b, gene_c], axis=-1)

    def test_m_computation(self):
        """Perform single computation by hand."""
        # 1) Compute component `a` by hand.
        A_ab = -ones(4)
        V_ab = A_ab.std()  # = 0.

        A_ac = log2(array([1., 0.6, 0.55555556, 0.6]))
        V_ac = A_ac.std()  # = 0.33819291902869014.

        M_a = (V_ab + V_ac) / 2

        # 2) Compute component `c` by hand using symmetry properties.
        # A_bc = 1 + A_ac = -A_cb
        A_cb = -(A_ac + 1)
        V_cb = A_cb.std()

        # The variance is the same since `A_ca` = - `A_ac`.
        V_ca = V_ac
        M_c = (V_cb + V_ca)/2

        # Compare function output with expected value.
        M = _m_numpy(self.gene_expression)

        assert_almost_equal(M[0], M_a)
        assert_almost_equal(M[2], M_c)

    def test_genorm(self):
        """Test backward elimination using M-values."""
        selected, m = _genorm_numpy(self.gene_expression, n_stop=2)

        # Since the first two components are equal up to a constant, the last component
        # has the largest M value. Therefore, geNorm should eliminate one (out of three)
        # components: the last.
        self.assertEqual(len(selected), 2)
        self.assertEqual(selected, [0, 1])

        # The remaining M-value should be zero.
        self.assertEqual(m.tolist(), [0.0, 0.0])

    def test_genorm_correct_index(self):
        """Check that the correct indices are selected."""
        # Expression example where the genes are sorted by columns. So it should keep
        # removing the first column in the submatrix.
        gene_d = array([1, 3, 5, 3])
        gene_c = gene_d * 2
        gene_b = gene_c + 1
        gene_a = gene_c - 1
        gene_expression = stack([gene_a, gene_b, gene_c, gene_d], axis=-1)
        selected, _ = _genorm_numpy(gene_expression, n_stop=2)

        self.assertEqual(len(selected), 2)
        assert_array_equal(selected, [2, 3])

        # Similarly, for a DataFrame.
        expression_frame = DataFrame(gene_expression, columns=[f'gene_{x}' for x in 'abcd'])
        genes, _ = genorm(expression_frame, n_stop=2)
        assert_array_equal(genes, ['gene_c', 'gene_d'])

    def test_domain(self):
        """Test that expression with zero counts raises an error."""
        self.gene_expression[1, 1] = 0
        with self.assertRaises(ValueError):
            _genorm_numpy(self.gene_expression)

        with self.assertRaises(ValueError):
            genorm(self.gene_expression)

    def test_data_types(self):
        """Test that both NumPy and Pandas data are accepted."""
        gene_frame = DataFrame(
            self.gene_expression,
            columns=['gene_a', 'gene_b', 'gene_c'],
            index=[f'sample_{i}' for i in range(1, 5)],
        )

        # Verify that the computed M values are the same.
        assert_array_equal(
            m_measure(gene_frame).to_numpy(),
            m_measure(self.gene_expression),
        )

        # And that the same genorm output.
        idx, m_values = genorm(self.gene_expression, n_stop=2)
        genes, m_series = genorm(gene_frame, n_stop=2)
        assert_array_equal(m_values, m_series.to_numpy())
        assert_array_equal(gene_frame.columns[idx], genes)
