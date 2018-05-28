#!/usr/bin/env python3

# adapted from wikipedia pseudocode
from collections import deque
from graph_util import parse_dag, spjoin

"""
Pseudocode adapted from Wikipedia:

L ← Empty list that will contain the sorted nodes
while there are unmarked nodes:
    visit(unmarked-node)

 function visit(node N)
    if N has a permanent mark then return
    if N has a temporary mark then stop (not a DAG)
    mark N temporarily
    for each node connected to N:
        visit(node)
    mark N permanently
    add N to head of L
"""


graph1 = parse_dag("""
    a -> b c d
    c -> d
""")

# 2 components
graph2 = parse_dag("""
    a -> b c d
    c -> d
    e -> g f q
""")

# cycle
graph3 = parse_dag("""
    a -> b c d
    c -> d e
    e -> g f q
    g -> c
""")

GRAY = 0    # temporary mark
BLACK = 1   # permanent

def topological(graph):
    nodes = deque()             # output -- ordered list
    entry_nodes = set(graph)
    state = {}

    def visit(node):
        """DFS
        If gray node is encountered, it means we have cycled back to it.
        If black node is encountered, we found it through an edge from a different entry node.
        """
        if state.get(node) is GRAY:
            raise ValueError("Cycle!")
        if state.get(node) is BLACK:
            return

        state[node] = GRAY
        for m in graph.get(node, ()):
            visit(m)
        state[node] = BLACK
        nodes.appendleft(node)

    while entry_nodes:
        n = entry_nodes.pop()
        visit(n)
    return nodes

def topological2(graph):
    """Slightly different version (logic is the same)."""
    nodes = deque()             # output -- ordered list
    entry_nodes = set(graph)
    S = {}                      # gray / black state

    def get_connections(N):
        return graph.get(N, ())

    def visit(N):
        """DFS
        If gray node is encountered, it means we have cycled back to it.
        If black node is encountered, we found it through an edge from a different entry node.
        """
        if S.get(N) is GRAY:
            raise ValueError("Cycle!")
        if S.get(N) is BLACK:
            return

        S[N] = GRAY
        [visit(M) for M in get_connections(N)]
        S[N] = BLACK
        nodes.appendleft(N)

    while entry_nodes:
        N = entry_nodes.pop()
        visit(N)
    return nodes

print(spjoin(topological(graph1)))
print(spjoin(topological(graph2)))
try:
    topological(graph3)
except ValueError as e:
    print (e)
