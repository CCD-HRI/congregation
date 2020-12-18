from congregation.lang import *
from congregation.dag import Dag
from congregation.dag.nodes.internal import *
from congregation.comp import PushDown, PushUp
from tests.utils import create_cols, compare_to_expected
import pytest


@pytest.mark.parametrize("party_data, expected", [
    (
        [
            {
                "col_names": ["a", "b"],
                "stored_with": {1},
                "plaintext_sets": [{1}, {1}],
                "trust_with_sets": [{1}, {1}]
            },
            {
                "col_names": ["c", "d"],
                "stored_with": {2},
                "plaintext_sets": [{2}, {2}],
                "trust_with_sets": [{2}, {2}]
            }
        ],
        {
            "node_order": [
                Create,
                Create,
                AggregateSumSquaresAndCount,
                AggregateSumSquaresAndCount,
                Concat,
                AggregateStdDev,
                AggregateStdDevLocalSqrt,
                Multiply,
                Collect
            ],
            "requires_mpc": [False, False, False, False, True, True, False, False, False],
            "ownership_data":[
                {
                    "stored_with": [{1}],
                    "plaintext_sets": [{1}, {1}],
                    "trust_with_sets": [{1}, {1}]
                },
                {
                    "stored_with": [{2}],
                    "plaintext_sets": [{2}, {2}],
                    "trust_with_sets": [{2}, {2}]
                },
                {
                    "stored_with": [{1}],
                    "plaintext_sets": [{1}, {1}, {1}, {1}],
                    "trust_with_sets": [{1}, {1}, {1}, {1}]
                },
                {
                    "stored_with": [{2}],
                    "plaintext_sets": [{2}, {2}, {2}, {2}],
                    "trust_with_sets": [{2}, {2}, {2}, {2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [set(), set(), set(), set()],
                    "trust_with_sets": [set(), set(), set(), set()]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}, {1, 2}, {1, 2}],
                    "trust_with_sets": [{1, 2}, {1, 2}, {1, 2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}, {1, 2}],
                    "trust_with_sets": [{1, 2}, {1, 2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}, {1, 2}],
                    "trust_with_sets": [{1, 2}, {1, 2}]
                }
            ]
        }
    ),
    (
        [
            {
                "col_names": ["a", "b"],
                "stored_with": {1},
                "plaintext_sets": [set(), set()],
                "trust_with_sets": [set(), set()]
            },
            {
                "col_names": ["c", "d"],
                "stored_with": {2},
                "plaintext_sets": [set(), set()],
                "trust_with_sets": [set(), set()]
            }
        ],
        {
            "node_order": [
                Create,
                Create,
                AggregateSumSquaresAndCount,
                AggregateSumSquaresAndCount,
                Concat,
                AggregateStdDev,
                AggregateStdDevLocalSqrt,
                Multiply,
                Collect
            ],
            "requires_mpc": [False, False, False, False, True, True, False, False, False],
            "ownership_data":[
                {
                    "stored_with": [{1}],
                    "plaintext_sets": [{1}, {1}],
                    "trust_with_sets": [{1}, {1}]
                },
                {
                    "stored_with": [{2}],
                    "plaintext_sets": [{2}, {2}],
                    "trust_with_sets": [{2}, {2}]
                },
                {
                    "stored_with": [{1}],
                    "plaintext_sets": [{1}, {1}, {1}, {1}],
                    "trust_with_sets": [{1}, {1}, {1}, {1}]
                },
                {
                    "stored_with": [{2}],
                    "plaintext_sets": [{2}, {2}, {2}, {2}],
                    "trust_with_sets": [{2}, {2}, {2}, {2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [set(), set(), set(), set()],
                    "trust_with_sets": [set(), set(), set(), set()]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}, {1, 2}, {1, 2}],
                    "trust_with_sets": [{1, 2}, {1, 2}, {1, 2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}, {1, 2}],
                    "trust_with_sets": [{1, 2}, {1, 2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}, {1, 2}],
                    "trust_with_sets": [{1, 2}, {1, 2}]
                }
            ]
        }
    ),
    (
        [
            {
                "col_names": ["a", "b"],
                "stored_with": {1},
                "plaintext_sets": [{1}, {1}],
                "trust_with_sets": [{1, 2}, {1}]
            },
            {
                "col_names": ["c", "d"],
                "stored_with": {2},
                "plaintext_sets": [{2}, {2}],
                "trust_with_sets": [{2}, {2}]
            }
        ],
        {
            "node_order": [
                Create,
                Create,
                AggregateSumSquaresAndCount,
                AggregateSumSquaresAndCount,
                Concat,
                AggregateStdDev,
                AggregateStdDevLocalSqrt,
                Multiply,
                Collect
            ],
            "requires_mpc": [False, False, False, False, True, True, False, False, False],
            "ownership_data":[
                {
                    "stored_with": [{1}],
                    "plaintext_sets": [{1}, {1}],
                    "trust_with_sets": [{1, 2}, {1}]
                },
                {
                    "stored_with": [{2}],
                    "plaintext_sets": [{2}, {2}],
                    "trust_with_sets": [{2}, {2}]
                },
                {
                    "stored_with": [{1}],
                    "plaintext_sets": [{1}, {1}, {1}, {1}],
                    "trust_with_sets": [{1, 2}, {1}, {1}, {1, 2}]
                },
                {
                    "stored_with": [{2}],
                    "plaintext_sets": [{2}, {2}, {2}, {2}],
                    "trust_with_sets": [{2}, {2}, {2}, {2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [set(), set(), set(), set()],
                    "trust_with_sets": [{2}, set(), set(), {2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}, {1, 2}, {1, 2}],
                    "trust_with_sets": [{1, 2}, {1, 2}, {1, 2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}, {1, 2}],
                    "trust_with_sets": [{1, 2}, {1, 2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}, {1, 2}],
                    "trust_with_sets": [{1, 2}, {1, 2}]
                }
            ]
        }
    ),
    (
        [
            {
                "col_names": ["a", "b"],
                "stored_with": {1, 2},
                "plaintext_sets": [set(), set()],
                "trust_with_sets": [set(), set()]
            },
            {
                "col_names": ["c", "d"],
                "stored_with": {1, 2},
                "plaintext_sets": [set(), set()],
                "trust_with_sets": [set(), set()]
            }
        ],
        {
            "node_order": [
                Create,
                Create,
                Concat,
                AggregateStdDev,
                AggregateStdDevLocalSqrt,
                Multiply,
                Collect
            ],
            "requires_mpc": [True, True, True, True, False, False, False],
            "ownership_data":[
                {
                    "stored_with": [{1, 2}],
                    "plaintext_sets": [set(), set()],
                    "trust_with_sets": [set(), set()]
                },
                {
                    "stored_with": [{1, 2}],
                    "plaintext_sets": [set(), set()],
                    "trust_with_sets": [set(), set()]
                },
                {
                    "stored_with": [{1, 2}],
                    "plaintext_sets": [set(), set()],
                    "trust_with_sets": [set(), set()]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}, {1, 2}, {1, 2}],
                    "trust_with_sets": [{1, 2}, {1, 2}, {1, 2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}, {1, 2}],
                    "trust_with_sets": [{1, 2}, {1, 2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}, {1, 2}],
                    "trust_with_sets": [{1, 2}, {1, 2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}, {1, 2}],
                    "trust_with_sets": [{1, 2}, {1, 2}]
                }
            ]
        }
    )
])
def test_agg_std_dev(party_data, expected):

    cols_in_one = create_cols(party_data[0])
    cols_in_two = create_cols(party_data[1])

    rel_one = create("in1", cols_in_one, party_data[0]["stored_with"])
    rel_two = create("in2", cols_in_two, party_data[1]["stored_with"])

    cc = concat([rel_one, rel_two], "concat", party_data[0]["col_names"])
    std_dev = aggregate(cc, "std_dev", [party_data[0]["col_names"][0]], party_data[0]["col_names"][1], "std_dev")
    mult = multiply(std_dev, "mult", party_data[0]["col_names"][0], [party_data[0]["col_names"][1], 7])
    collect(mult, {1, 2})

    d = Dag({rel_one, rel_two})
    pd = PushDown()
    pd.rewrite(d)
    pu = PushUp()
    pu.rewrite(d)

    compare_to_expected(d, expected)
