from congregation.lang import *
from congregation.dag import Dag
from congregation.comp import PushDown
from tests.utils import create_cols, compare_to_expected
import pytest


"""
Tests for correct propagation of the following relation-level
and column-level attributes after the PushDown() phase of the
compiler has been run:
    - DAG node order
    - node.requires_mpc() attribute
    - relation-level stored_with sets
    - column-level plaintext sets
    - column-level trust_with sets
    - column ordering in cases where columns 
    are reordered as part of the Op.
"""


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
            "node_order": [Create, Create, Project, Project, Concat, Collect],
            "requires_mpc": [False, False, False, False, True, False],
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
                    "plaintext_sets": [{1}],
                    "trust_with_sets": [{1}]
                },
                {
                    "stored_with": [{2}],
                    "plaintext_sets": [{2}],
                    "trust_with_sets": [{2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [set()],
                    "trust_with_sets": [set()]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}],
                    "trust_with_sets": [{1, 2}]
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
            "node_order": [Create, Create, Project, Project, Concat, Collect],
            "requires_mpc": [False, False, False, False, True, False],
            "ownership_data": [
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
                    "plaintext_sets": [{1}],
                    "trust_with_sets": [{1}]
                },
                {
                    "stored_with": [{2}],
                    "plaintext_sets": [{2}],
                    "trust_with_sets": [{2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [set()],
                    "trust_with_sets": [set()]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}],
                    "trust_with_sets": [{1, 2}]
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
                "trust_with_sets": [{1}, {1, 2}]
            },
            {
                "col_names": ["c", "d"],
                "stored_with": {2},
                "plaintext_sets": [{2}, {2}],
                "trust_with_sets": [{2}, {2}]
            }
        ],
        {
            "node_order": [Create, Create, Project, Project, Concat, Collect],
            "requires_mpc": [False, False, False, False, True, False],
            "ownership_data": [
                {
                    "stored_with": [{1}],
                    "plaintext_sets": [{1}, {1}],
                    "trust_with_sets": [{1}, {1, 2}]
                },
                {
                    "stored_with": [{2}],
                    "plaintext_sets": [{2}, {2}],
                    "trust_with_sets": [{2}, {2}]
                },
                {
                    "stored_with": [{1}],
                    "plaintext_sets": [{1}],
                    "trust_with_sets": [{1}]
                },
                {
                    "stored_with": [{2}],
                    "plaintext_sets": [{2}],
                    "trust_with_sets": [{2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [set()],
                    "trust_with_sets": [set()]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}],
                    "trust_with_sets": [{1, 2}]
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
            "node_order": [Create, Create, Project, Project, Concat, Collect],
            "requires_mpc": [False, False, False, False, False, False],
            "ownership_data": [
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
                    "plaintext_sets": [{1}],
                    "trust_with_sets": [{1, 2}]
                },
                {
                    "stored_with": [{2}],
                    "plaintext_sets": [{2}],
                    "trust_with_sets": [{2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [set()],
                    "trust_with_sets": [{2}]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}],
                    "trust_with_sets": [{1, 2}]
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
            "node_order": [Create, Create, Concat, Project, Collect],
            "requires_mpc": [True, True, True, True, False],
            "ownership_data": [
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
                    "stored_with": [{1, 2}],
                    "plaintext_sets": [set()],
                    "trust_with_sets": [set()]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}],
                    "trust_with_sets": [{1, 2}]
                }
            ]
        }
    )
])
def test_project(party_data, expected):

    cols_in_one = create_cols(party_data[0])
    cols_in_two = create_cols(party_data[1])

    rel_one = create("in1", cols_in_one, party_data[0]["stored_with"])
    rel_two = create("in2", cols_in_two, party_data[1]["stored_with"])

    cc = concat([rel_one, rel_two], "concat", party_data[0]["col_names"])
    p = project(cc, "proj", [party_data[0]["col_names"][0]])
    collect(p, {1, 2})

    d = Dag({rel_one, rel_two})
    pd = PushDown()
    pd.rewrite(d)

    compare_to_expected(d, expected)


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
            "node_order": [Create, Create, Project, Project, Concat, Collect],
            "requires_mpc": [False, False, False, False, True, False],
            "ownership_data":[
                {
                    "stored_with": [{1}],
                    "plaintext_sets": [{1}, {1}],
                    "trust_with_sets": [{1}, {1}],
                    "col_names": ["a", "b"]
                },
                {
                    "stored_with": [{2}],
                    "plaintext_sets": [{2}, {2}],
                    "trust_with_sets": [{2}, {2}],
                    "col_names": ["c", "d"]
                },
                {
                    "stored_with": [{1}],
                    "plaintext_sets": [{1}, {1}],
                    "trust_with_sets": [{1}, {1}],
                    "col_names": ["b", "a"]
                },
                {
                    "stored_with": [{2}],
                    "plaintext_sets": [{2}, {2}],
                    "trust_with_sets": [{2}, {2}],
                    "col_names": ["d", "c"]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [set(), set()],
                    "trust_with_sets": [set(), set()],
                    "col_names": ["b", "a"]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}, {1, 2}],
                    "trust_with_sets": [{1, 2}, {1, 2}],
                    "col_names": ["b", "a"]
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
            "node_order": [Create, Create, Project, Project, Concat, Collect],
            "requires_mpc": [False, False, False, False, True, False],
            "ownership_data":[
                {
                    "stored_with": [{1}],
                    "plaintext_sets": [{1}, {1}],
                    "trust_with_sets": [{1}, {1}],
                    "col_names": ["a", "b"]
                },
                {
                    "stored_with": [{2}],
                    "plaintext_sets": [{2}, {2}],
                    "trust_with_sets": [{2}, {2}],
                    "col_names": ["c", "d"]
                },
                {
                    "stored_with": [{1}],
                    "plaintext_sets": [{1}, {1}],
                    "trust_with_sets": [{1}, {1}],
                    "col_names": ["b", "a"]
                },
                {
                    "stored_with": [{2}],
                    "plaintext_sets": [{2}, {2}],
                    "trust_with_sets": [{2}, {2}],
                    "col_names": ["d", "c"]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [set(), set()],
                    "trust_with_sets": [set(), set()],
                    "col_names": ["b", "a"]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}, {1, 2}],
                    "trust_with_sets": [{1, 2}, {1, 2}],
                    "col_names": ["b", "a"]
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
            "node_order": [Create, Create, Concat, Project, Collect],
            "requires_mpc": [True, True, True, True, False],
            "ownership_data": [
                {
                    "stored_with": [{1, 2}],
                    "plaintext_sets": [set(), set()],
                    "trust_with_sets": [set(), set()],
                    "col_names": ["a", "b"]
                },
                {
                    "stored_with": [{1, 2}],
                    "plaintext_sets": [set(), set()],
                    "trust_with_sets": [set(), set()],
                    "col_names": ["c", "d"]
                },
                {
                    "stored_with": [{1, 2}],
                    "plaintext_sets": [set(), set()],
                    "trust_with_sets": [set(), set()],
                    "col_names": ["a", "b"]
                },
                {
                    "stored_with": [{1, 2}],
                    "plaintext_sets": [set(), set()],
                    "trust_with_sets": [set(), set()],
                    "col_names": ["b", "a"]
                },
                {
                    "stored_with": [{1}, {2}],
                    "plaintext_sets": [{1, 2}, {1, 2}],
                    "trust_with_sets": [{1, 2}, {1, 2}],
                    "col_names": ["b", "a"]
                }
            ]
        }
    )
])
def test_project_reorder_cols(party_data, expected):

    cols_in_one = create_cols(party_data[0])
    cols_in_two = create_cols(party_data[1])

    rel_one = create("in1", cols_in_one, party_data[0]["stored_with"])
    rel_two = create("in2", cols_in_two, party_data[1]["stored_with"])

    cc = concat([rel_one, rel_two], "concat", party_data[0]["col_names"])
    p = project(cc, "proj", party_data[0]["col_names"][::-1])
    collect(p, {1, 2})

    d = Dag({rel_one, rel_two})
    pd = PushDown()
    pd.rewrite(d)

    compare_to_expected(d, expected)

    zip_col_names = zip(d.top_sort(), [e["col_names"] for e in expected["ownership_data"]])
    col_name_checks = [[c.name for c in z[0].out_rel.columns] == z[1] for z in zip_col_names]
    assert all(col_name_checks)
