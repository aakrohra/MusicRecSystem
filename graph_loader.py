"""CSC111 Project 2 - Graph Loader

Module Description: Creates a weighted graph using data from a CSV file.

This file is Copyright (c) 2024 Aakaash Rohra, Daniel Xie, Ethan Chiu, and Jackie Chen.
"""
from __future__ import annotations
from typing import Any, Union
import pandas


class _Vertex: 
    """A vertex in a song similarity graph.

    Each vertex item is the instance id of a song, which is represented as a float.

    Instance Attributes:
        - item: The data stored in this vertex, representing the instance id of a song.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Any
    neighbours: set[_Vertex]

    def __init__(self, item: Any) -> None:
        """Initialize a new vertex with the given item.

        This vertex is initialized with no neighbours.
        """
        self.item = item
        self.neighbours = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)


class Graph:
    """A graph used to represent a song similarity network.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self) -> set:
        """Return a set of all vertex items in this graph.
        """
        return set(self._vertices.keys())


class _WeightedVertex(_Vertex):
    """A vertex in a weighted song similarity graph.

    Each vertex item is the instance id of a song, which is represented as a float.
    The weights are a "similarity score" between the two songs, which is calculated by
    finding the song's absolute difference between their ratings in each category, and
    summing them.

    Instance Attributes:
        - item: The data stored in this vertex, representing the instance id of a song.
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Any
    neighbours: dict[_WeightedVertex, Union[int, float]]

    def __init__(self, item: Any) -> None:
        """Initialize a new vertex with the given item.

        This vertex is initialized with no neighbours.
        """
        super().__init__(item)
        self.neighbours = {}


class WeightedGraph(Graph):
    """A weighted graph used to represent a song similarity network that keeps
    track of the similarity between each song.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _WeightedVertex object.
    _vertices: dict[Any, _WeightedVertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

        # This call isn't necessary, except to satisfy PythonTA.
        Graph.__init__(self)

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
        """
        if item not in self._vertices:
            self._vertices[item] = _WeightedVertex(item)

    def add_edge(self, item1: Any, item2: Any, weight: float = 0.0) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def get_weight(self, item1: Any, item2: Any) -> Union[int, float]:
        """Return the weight of the edge between the given items.

        Return 0 if item1 and item2 are not adjacent.

        Preconditions:
            - item1 and item2 are vertices in this graph
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        return v1.neighbours.get(v2, 0)

    def average_weight(self, item: Any) -> float:
        """Return the average weight of the edges adjacent to the vertex corresponding to item.

        Raise ValueError if item does not corresponding to a vertex in the graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return sum(v.neighbours.values()) / len(v.neighbours)
        else:
            raise ValueError

    def get_song_recommendations(self, song: float) -> list[float]:
        """
        Returns the instance ids of the songs most similar to the input song provided.
        The returned list is given in order of most similar to least.

        Raise ValueError if item does not correspond to a vertex in the graph.
        """
        if song not in self._vertices:
            raise ValueError
        input_vertex = self._vertices[song]
        sorted_lst = [u.item for u in self._ascending_sort_dictionary(input_vertex.neighbours)]
        return sorted_lst
        # selection sorting neighbours (should be fine bc it's a small selection?)

    def _ascending_sort_dictionary(self, d: dict) -> list:
        """
        Helper function for get_song_recommendations()

        Returns a list containing the keys of d and sorted in ascending order by the values of d.
        """
        d_new = dict(d)
        sorted_lst = []
        item = Any

        for _ in range(len(d_new)):
            smallest = 99999
            for key in d_new:
                if d_new[key] < smallest:
                    item = key
                    smallest = d_new[key]
            sorted_lst.append(item)
            del d_new[item]

        return sorted_lst


def load_graph(raw_data: pandas.DataFrame, genre: str) -> WeightedGraph:
    """Return a weighted song similarity graph corresponding to the given
    dataset containing only one genre of song.

    Preconditions:
        - file is the path to a CSV file corresponding to the song ratings data.
    """
    data = raw_data[(raw_data.music_genre == genre)].copy()
    graph = WeightedGraph()

    for s in data.iterrows():        # adds all the songs in data
        graph.add_vertex(s[1]['instance_id'])

    for s in data.iterrows():  # select a song
        data['difference'] = abs(data['acousticness'] - s[1]['acousticness'])  # create a difference column
        for c in data.columns[4:9]:  # select the different categories
            data['difference'] += abs(data[c] - s[1][c])  # adds the differences of all of them to the diff score
        sort_by_similar = data.sort_values('difference', ascending=True)  # sorts the differences in ascending order
        for i in range(16):  # iterates 16 times
            if s[1]['instance_id'] != sort_by_similar.iloc[i]['instance_id']:  # checks if it is the selected song
                graph.add_edge(s[1]['instance_id'],
                               sort_by_similar.iloc[i]['instance_id'],
                               sort_by_similar.iloc[i]['difference'])
                # adds edge btwn select and song

    return graph


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pandas'],
        'max-line-length': 120
    })
