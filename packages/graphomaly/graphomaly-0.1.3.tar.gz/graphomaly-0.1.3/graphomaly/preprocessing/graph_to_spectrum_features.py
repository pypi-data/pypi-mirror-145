# Copyright (c) 2022 Andrei Pătrașcu <andrei.patrascu@fmi.unibuc.ro>
# Copyright (c) 2021 Bogdan Dumitrescu <bogdan.dumitrescu@upb.ro>
# Copyright (c) 2022 Paul Irofti <paul@irofti.net>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import logging

import networkx as nx
import numpy as np
import pandas as pd
from scipy.sparse.linalg import svds


def graph_to_spectrum_features(
    G,
    FULL_egonets=True,
    IN_egonets=False,
    summable_attributes=[],
    n_values=5,
):
    """Extract spectrum features from input graph based in the singular values of the associated Laplacians.

     Parameters
     ----------
     G : networkx DiGraph or pandas DataFrame or matrix
         Transactions graph. It must have the following edge attributes:
         * 'cumulated_amount': the cumulated amount of transactions from source to destination node
         * 'n_transactions': number of transactions between the two nodes
         It can have other attributes.
         A dataframe is immediately converted to Networkx graph, so there is no advantage in giving a dataframe.
         The columns for nodes forming an edge should be named "id_source" and "id_destination".
         A matrix must have the following meanings for its first columns (in this order):
         id_source, id_destination, cumulated_amount, n_transactions.
         Further columns are disregarded. Each row represents an edge.

     FULL_egonets : bool, default=True
         Whether full undirected egonets (with radius 1) are considered

     IN_egonets : bool, default=False
         Whether in or out egonets are considered, with respect to the current node.
         Is considered only if FULL_egonets=False.

     summable_attributes: list
         List of edge attributes to be summed as adjacent nodes features.
         The name of the feature is the same as the name of the edge attribute.
         The attributes must be present in all edges; no check is made.
         If the input is a matrix, then summable_attributes must contain column numbers.

     Returns
     -------
     node_features: matrix
         Contains features defined by the Laplacian spectrum
         (singular values) of each egonet.
         Two Laplacian matrices are computed, corresponding to attributes
         cumulated_amount and n_transactions.
         The features on each node are formed by concatenation of
         singular values spectrum of the two Laplacian matrices.

    node_ids: vector
        Contains node ids, sorted increasingly, corresponding to the rows
        of node_features.
    """

    # These first conversions are the same as in graph_to_features.py

    # matrix_io = False
    Ns = len(summable_attributes)

    if isinstance(G, pd.DataFrame):  # if dataframe, convert to graph
        G = nx.from_pandas_edgelist(
            df=G,
            source="id_source",
            target="id_destination",
            edge_attr=True,
            create_using=nx.DiGraph,
        )
    elif isinstance(G, np.ndarray):  # if matrix, convert to graph
        # matrix_io = True
        # summable_attributes = []        # ignore summable attributes, if any (a warning???)
        # the easy way: convert first matrix to dataframe, then dataframe to graph
        if Ns == 0:  # if no other attributes, convert directly
            G = pd.DataFrame(
                G[:, 0:4],
                columns=[
                    "id_source",
                    "id_destination",
                    "cumulated_amount",
                    "n_transactions",
                ],
            )
        else:  # first copy attributes columns in another array
            Ga = np.copy(G[:, summable_attributes])
            G = pd.DataFrame(
                G[:, 0:4],
                columns=[
                    "id_source",
                    "id_destination",
                    "cumulated_amount",
                    "n_transactions",
                ],
            )
            for i in range(Ns):  # add columns for attributes
                G[str(summable_attributes[i])] = Ga[:, i]
                summable_attributes[i] = str(summable_attributes[i])
        # convert dataframe to graph
        G = nx.from_pandas_edgelist(
            df=G,
            source="id_source",
            target="id_destination",
            edge_attr=True,
            create_using=nx.DiGraph,
        )
    else:
        logging.warning("Wrong data type for G")

    if not FULL_egonets and IN_egonets:  # reverse graph if in egonets are desired
        G = G.reverse(copy=False)

    logging.info(f"Graph info {nx.info(G)}")

    Nn = G.number_of_nodes()

    # store features in matrix (it's faster)
    degGarray = np.array([val for (node, val) in G.degree()])
    degG = degGarray.max()

    node_features = np.zeros((Nn, 2 * degG))
    node_ids = np.zeros(Nn)

    # go over all nodes and extract features
    row = 0
    for node in G:
        # generate full egonet with ad hoc construction (networkx is slow!)
        if FULL_egonets:
            No = G.successors(node)
            Ni = G.predecessors(node)
            enodes = [node]  # create list of egonets nodes
            enodes.extend(No)
            enodes.extend(Ni)
            Gs = G.subgraph(enodes)
        else:  # out or in egonets
            Gs = nx.generators.ego.ego_graph(G, node, radius=1)

        L_ego1 = nx.adjacency_matrix(
            Gs, weight="cumulated_amount"
        )  # weight requires array of edge weights
        L_ego1 = L_ego1.toarray().astype(float)

        D = np.diag(np.sum(L_ego1, axis=1))
        L_ego1 = D - L_ego1  # Laplacian matrix is computed

        U, s1, V = svds(L_ego1, n_values)  # Compute SVD of Laplacian matrix 1
        s1 = np.sort(s1)
        node_features[row, 0 : len(s1)] = s1

        L_ego2 = nx.adjacency_matrix(Gs, weight="n_transactions")
        L_ego2 = L_ego2.toarray().astype(float)

        D = np.diag(np.sum(L_ego2, axis=1))
        L_ego2 = D - L_ego2  # Laplacian matrix is computed

        U, s2, V = svds(L_ego2, n_values)  # Compute SVD of egonet Laplacian matrix
        s2 = np.sort(s2)
        node_features[row, degG : degG + len(s2)] = s2

        node_ids[row] = node
        row = row + 1

    # sort on id
    ii = np.argsort(node_ids)
    node_ids = node_ids[ii]
    node_features = node_features[ii]

    return node_features, node_ids
