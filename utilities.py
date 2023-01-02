#!/usr/bin/env python
import operator
import numpy as np
import os



def read_fasta_sequences(path: str):
    try:
        with open(path, "r", encoding='utf-8-sig') as file:
            # Read the text from a file
            sequences = file.read()
            print(sequences)
    except Exception as e:
        if "No such file or directory" in e.__str__():
            raise Exception("**ERROR** No such file or directory")

    sequences_group = {}
    for line in sequences:
        if(line.startswith(">")):
            key = line


def traverse(tree, node, queue, queues):
    if node == (0, 0):
        queues.append(list(queue))
        queue.clear()
        return
    for nodes in tree[node]:
        old_queue = list(queue)
        queue.append(nodes)
        traverse(tree, nodes, queue, queues)
        queue = old_queue

def global_alignment(sequence_1:str, sequence_2:str, match:int=1, mismatch:int=1, gap:int=1):
    """
    The Needleman-Wunsch Algorithm
    ==============================
    This is a dynamic programming algorithm for finding the optimal alignment of
    two strings.
    
    Arguments
    -------
    seq1: first sequence (Must be combination of A,C,G,T)
    seq2: seconde sequence (Must be combination of A,C,G,T)
    match: matching score
    mismatch: mismatching score
    gap: gapping score

    Returns
    -------
    rx: first sequence alignment
    ry: second sequence alignment

    Example
    -------
        >>> x = "GATTACA"
        >>> y = "GCATGCU"
        >>> global_alignment(x, y)
        G-ATTACA
        GCA-TGCU
    """

    if type(sequence_1) != str:
        sequence_1 = "".join(sequence_1)
    
    if type(sequence_2) != str:
        sequence_2 = "".join(sequence_2)

    if type(match) == str:
        match = int(match)

    if type(mismatch) == str:
        mismatch = int(mismatch)

    if type(gap) == str:
        gap = int(gap)

    N = len(sequence_1) + 1
    M = len(sequence_2) + 1

    # STEP 1: CONSTRUCTING AND FILLING THE GRID
    # initialization with zeros
    matrix = [[0] * N for _ in range(M)]

    # initialize first row and column
    for i in range(M):
        matrix[i][0] = i * mismatch
    for i in range(N):
        matrix[0][i] = i * mismatch

    # initialize the tree dictionary, which will keep the paths from nodes
    tree = {}
    for i in range(1, M):
        tree.setdefault((i, 0), [(i - 1, 0)])
    for i in range(1, N):
        tree.setdefault((0, i), [(0, i - 1)])

    # fill the numbers of each element
    for i in range(1, M):
        for j in range(1, N):
            diagonal = 0
            if sequence_1[j - 1] == sequence_2[i - 1]:
                diagonal += match
            else:
                diagonal += mismatch

            diagonal += matrix[i - 1][j - 1]

            # Getting values of neighbours
            left = matrix[i][j - 1] + gap
            up = matrix[i - 1][j] + gap
            matrix[i][j] = max(diagonal, up, left)

            # Getting indices of neighbours
            left_id = (i, j - 1)
            up_id = (i - 1, j)
            diagonal_id = (i - 1, j - 1)
            indices = [diagonal_id, up_id, left_id]

            # Getting maximum indices
            max_indices = []
            values = [diagonal, up, left]
            for k in range(len(values)):
                if matrix[i][j] == values[k]:
                    max_indices.append(indices[k])

            tree.setdefault((i, j), max_indices)

    # Step 2: GET THE POSSIBLE ALIGNMENTS, AND TRACE BACK TO THE FIRST ELEMENT.
    # queue variable represent a path that can be taken from bottom right to top left cell
    # queues variable represent all optimal paths
    # tree is traversed in depth-first recursive manner
    queues = []
    traverse(tree, (len(sequence_2), len(sequence_1)), [], queues)
    for queue in queues:
        queue.insert(0, (M - 1, N - 1))

    # STEP 3: FROM ARROWS TO STRING (DETERMINE GAP POSITIONS)
    optimal = []
    for queue in queues:
        seq_a = []
        seq_b = []
        ind_a = N - 1
        ind_b = M - 1
        for index in range(len(queue)):
            if index == len(queue) - 1:
                optimal.append([seq_a, seq_b])
                break
            move = tuple(map(operator.sub, queue[index], queue[index + 1]))
            if move == (1, 1):
                seq_a.insert(0, sequence_1[ind_a - 1])
                seq_b.insert(0, sequence_2[ind_b - 1])
                ind_a -= 1
                ind_b -= 1
            if move == (0, 1):
                seq_a.insert(0, sequence_1[ind_a - 1])
                seq_b.insert(0, "-")
                ind_a -= 1
            if move == (1, 0):
                seq_a.insert(0, "-")
                seq_b.insert(0, sequence_2[ind_b - 1])
                ind_b -= 1
    return optimal

def local_alignment(seq1:str, seq2:str, match:int=1, mismatch:int=1, gap:int=1):
    """
    The Smith-Waterman Algorithm
    ==============================
    This is a dynamic programming algorithm for finding the optimal alignment of
    two strings.
    
    Arguments
    -------
    seq1: first sequence (Must be combination of A,C,G,T)
    seq2: second sequence (Must be combination of A,C,G,T)
    match: matching score
    mismatch: mismatching score
    gap: gapping score

    Returns
    -------
    rx: first sequence alignment
    ry: second sequence alignment

    Example
    -------
        >>> x = "GATTACA"
        >>> y = "GCATGCU"
        >>> global_alignment(x, y)
        G-ATTACA
        GCA-TGCU
    """

    if type(seq1) != str:
        seq1 = "".join(seq1)
    
    if type(seq2) != str:
        seq2 = "".join(seq2)

    nx = len(seq1)
    ny = len(seq2)