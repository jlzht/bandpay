from abc import ABC, abstractmethod
from fastapi import APIRouter


class Routes(ABC):
    def __init__(self, database):
        self.database = database
        self.router = APIRouter()
        self._register_routes()

    @abstractmethod
    def _register_routes(self):
        """Abstract method to register API routes"""
        pass
