"""
Submodule for graph importer.
"""

from .factories import _get_importer_factory
from .interfaces import GraphImporterInterface


def _get_importer(graph) -> GraphImporterInterface:
    """function to get importer from graph"""
    return _get_importer_factory(graph).get_graph_importer()


def import_(graph):
    """function that uses graph importer and calls it with provided graph"""
    return _get_importer(graph)(graph)
