"""
Includes corresponding factories for the graph importers.
"""

from importlib import import_module

from .importer import \
    GraphToolsGraphImporter, \
    IGraphGraphImporter, \
    NetworkxGraphImporter, \
    PyGraphvizGraphImporter
from .interfaces import \
    GraphImporterInterface, \
    GraphImporterFactoryInterface


class GraphToolsGraphImporterFactory(GraphImporterFactoryInterface):
    """factory providing graph tools graph importer"""

    def get_graph_importer(self) -> GraphImporterInterface:
        """return new graph tools graph importer"""
        return GraphToolsGraphImporter()


class IGraphGraphImporterFactory(GraphImporterFactoryInterface):
    """factory providing igraph graph importer"""

    def get_graph_importer(self) -> GraphImporterInterface:
        """return new igraph graph importer"""
        return IGraphGraphImporter()


class NetworkxGraphImporterFactory(GraphImporterFactoryInterface):
    """factory providing networkx graph importer"""

    def get_graph_importer(self) -> GraphImporterInterface:
        """return new networkx graph importer"""
        return NetworkxGraphImporter()


class PyGraphvizGraphImporterFactory(GraphImporterFactoryInterface):
    """factory providing pygraphviz graph importer"""

    def get_graph_importer(self) -> GraphImporterInterface:
        """return new pygraphviz graph importer"""
        return PyGraphvizGraphImporter()


def _try_import(name: str):
    try:
        module = import_module(name)
        try:
            return module.__getattribute__('Graph')
        except AttributeError:
            # pygraphviz is special
            return module.__getattribute__('AGraph')
    except ImportError:
        return None


def _append_graph_type(module_name, graph_factory, types):
    graph_type = _try_import(module_name)
    if graph_type:
        types[graph_type] = graph_factory


def _get_importer_factory(graph) -> GraphImporterFactoryInterface:
    """function to select factory based on graph type"""
    types = {}
    module_name_to_factory_mapping = {
        'graph_tool': GraphToolsGraphImporterFactory(),
        'igraph': IGraphGraphImporterFactory(),
        'networkx': NetworkxGraphImporterFactory(),
        'pygraphviz': PyGraphvizGraphImporterFactory()
    }

    for module_name, graph_factory in module_name_to_factory_mapping.items():
        _append_graph_type(module_name, graph_factory, types)

    for graph_type, graph_factory in types.items():
        if isinstance(graph, graph_type):
            return graph_factory

    raise NotImplementedError('Could not find a graph importer factory for type {}'.format(type(graph)))
