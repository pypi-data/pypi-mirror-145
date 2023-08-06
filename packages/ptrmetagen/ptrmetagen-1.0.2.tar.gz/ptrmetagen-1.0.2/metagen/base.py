# general and helper function and classe

from pathlib import Path
from typing import Union, Optional, Any, List
from pydantic import BaseModel, Field, root_validator
from abc import ABC, abstractmethod
from uuid import UUID, uuid4
import json
from functools import wraps


# helper func
def create_file(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def check_path(path: Union[Path, str]) -> Path:
    if not isinstance(path, Path):
        return Path(path)
    return path


def prepare_data_for_leaf(obj: dict) -> dict:
    data = obj.pop('data')
    obj.update(data)
    return obj


# helper class
class SingletonMeta(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)


# base
class LeafABC(BaseModel, ABC):

    @abstractmethod
    def __nodes__(self) -> str:
        pass

    @property
    @abstractmethod
    def hash_attrs(self) -> tuple:
        pass


# register
class Register(BaseModel):
    hashs: dict = Field(default_factory=dict)
    uuid: dict = Field(default_factory=dict)
    name: dict = Field(default_factory=dict)

    def add(self, element: BaseModel) -> None:
        if not self.check_register(element):
            self.hashs.update({hash(element): element})
            self.uuid.update({element.key: element})
            self.name.update({element.nameInternal: element})
        else:
            raise ValueError(f'PTR element "{element.__class__.__name__}" with nameInternal: {element.nameInternal}, '
                             f'key: {element.key} and hash: {hash(element)} already exist')

    def check_register(self, obj: BaseModel) -> bool:
        return all([self.hashs.get(hash(obj)),
                    self.uuid.get(obj.key),
                    self.name.get(obj.nameInternal)])

    def get_by_name(self, name: str) -> LeafABC:
        return self.name.get(name)

    def get_by_hash(self, hash: int) -> LeafABC:
        return self.hashs.get(hash)


register = Register()


def exist_in_register(element):
    @wraps(element)
    def checkting_register(*args, **kwargs):
        instance = element(*args, **kwargs)
        if register.check_register(instance):
            return register.get_by_hash(hash(instance))
        else:
            register.add(instance)
            return instance

    return checkting_register


# element base parent
class Leaf(LeafABC):
    key: Optional[Union[UUID, str]] = Field(default_factory=uuid4)

    def to_dict(self):
        data = self.dict(by_alias=True, exclude_none=True)
        key = data.pop('key')
        return {"key": str(key), "data": data}

    @root_validator(pre=True)
    def set_key(cls, values: dict) -> dict:
        return {k: (v.key if isinstance(v, Leaf) else v) for k, v in values.items()}

    def __hash__(self) -> int:
        return hash(tuple(self.__dict__.get(attr) for attr in self.hash_attrs))


# serialization & deserialization
class Serializer(BaseModel, ABC):

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def to_json(self, path: Union[Path, str]) -> None:
        pass


class DeSerializer(BaseModel, ABC):

    @abstractmethod
    def load(self, path: Path) -> None:
        pass


class JSONSerializer(Serializer):
    structure: dict = Field(default={})

    def to_dict(self) -> dict:
        for _, element in register.hashs.items():
            nodes = element.__nodes__().split('.')
            self.set_node(self.structure, nodes, element)
        return self.structure

    def set_node(self, structure: dict, nodes: list, element: Leaf):
        node = nodes.pop(0)
        if len(nodes) > 0:
            if not structure.get(node):
                structure[node] = {}
            self.set_node(structure[node], nodes, element)
        else:
            if not structure.get(node):
                structure[node] = []
            structure[node].append(element.to_dict())

    def to_json(self, path: Union[Path, str]) -> None:
        structure = self.to_dict()

        path = check_path(path)

        if not path.parent:
            create_file(path.parent)

        with open(path, 'w') as file:
            json.dump(structure, file, indent=6, cls=UUIDEncoder)


from metagen.elements import ElementFactory, element_factory


class JSONDeserializer(DeSerializer):
    factory: ElementFactory = element_factory

    def load(self, path: Path) -> None:

        path = check_path(path)

        with open(path, 'r') as file:
            obj = json.load(file)

        for node, structure in obj.items():
            self._parse(node, structure)

    def _parse(self, nodes: str, obj: Union[dict, list]) -> None:

        if isinstance(obj, dict):
            for node, structure in obj.items():
                self._parse(f'{nodes}.{node}', structure)
        elif isinstance(obj, list):
            for data in obj:
                element = self.factory.create_element(nodes, data)
                register.add(element)


class Generator(BaseModel):
    serializer: Serializer = Field(default=JSONSerializer())
    deserializer: DeSerializer = Field(default=JSONDeserializer())

    def load(self, path: Path) -> None:
        self.deserializer.load(path)

    def to_dict(self) -> dict:
        return self.serializer.to_dict()

    def to_json(self, path: Path) -> None:
        self.serializer.to_json(path)

    def get_element_by_nameInternal(self, name: str) -> LeafABC:
        if register.get_by_name(name):
            return register.get_by_name(name)
        else:
            raise ValueError(f'Element with nameInternal {name} did not find')

    @property
    def register(self):
        return register

    def get_elements_by_type(self, element: Leaf) -> List[Leaf]:
        return [v for k, v in self.register.name.items() if isinstance(v, element.__wrapped__)]

    def get_elements_by_name(self, name: str) -> List[Leaf]:
        return [v for k, v in self.register.name.items() if k.__contains__(name)]
