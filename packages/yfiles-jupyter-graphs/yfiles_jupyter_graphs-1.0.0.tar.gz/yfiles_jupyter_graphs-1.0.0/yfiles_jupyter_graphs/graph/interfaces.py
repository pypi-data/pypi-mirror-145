"""
Common interfaces for graph importers.
"""

from abc import ABC, abstractmethod
from typing import Tuple, List, Dict


class GraphImporterInterface(ABC):
    """Common interface for graph importers."""
    def __init__(self, _type) -> None:
        super().__init__()
        self._type = _type

    @abstractmethod
    def _import(self, graph) -> Tuple[List[Dict], List[Dict], bool]:
        """import graph"""

    def __call__(self, graph):
        assert isinstance(graph, self._type)
        return self._import(graph)


class GraphImporterFactoryInterface(ABC):
    """Common factory interface for graph importers.

    Provides only one graph importer and
    does not maintain any of the instances it creates.
    """

    @abstractmethod
    def get_graph_importer(self) -> GraphImporterInterface:
        """return a new graph importer instance"""
