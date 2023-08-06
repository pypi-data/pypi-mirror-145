from abc import ABC, abstractmethod
from libqtile.config import Key, Group, Drag
from typing import List, Union
from libqtile.lazy import lazy
from pydantic import BaseModel
from juselara_qtile.dataclasses import Keys

Callback = Union[Key, Group, Drag]

class KeyLoader(ABC):
    keys: List[Callback]

    @abstractmethod
    def load(self, kind: str, keys: List[str]):
        ...

    @abstractmethod
    def extract(self) -> List[Callback]:
        ...

class KeyLoaderImpl(KeyLoader):
    def __init__(self):
        self.keys = []

    @abstractmethod
    def load(self, kind: str, keys: List[str]):
        ...

    def extract(self) -> List[Callback]:
        return self.keys

class SingleKeyLoader(KeyLoaderImpl):
    def load(self, kind: str, keys: List[str]):
        func = eval(f"lazy.layout.{kind}")
        self.keys.append(Key([keys[0]], keys[1], func()))

class DoubleKeyLoader(KeyLoaderImpl):
    def load(self, kind: str, keys: List[str]):
        func = eval(f"lazy.layout.{kind}")
        self.keys.append(Key([keys[0], keys[1]], keys[2], func()))

class StopKeyLoader(KeyLoaderImpl):
    def load(self, kind: str, keys: List[str]):
        func = eval(f"lazy.{kind}")
        self.keys.append(Key([keys[0], keys[1]], keys[2], func()))

class KeySpawnLoader(KeyLoaderImpl):
    def load(self, kind: str, keys: List[str]):
        func = lazy.spawn(kind)
        self.keys.append(Key([keys[0]], keys[1], func()))

class UtilsKeyLoader(KeyLoaderImpl):
    funcs = {
            "normalize": lazy.layout.normalize,
            "maximize": lazy.layout.maximize,
            "next_screen": lazy.screen.next,
            "kill": lazy.window.kill,
            "toggle_floating": lazy.window.toggle_floating,
            "fullscreen": lazy.window.toggle_fullscreen,
            "next_window": lazy.group.next_window,
            "prev_window": lazy.group.prev_window,
            "restart": lazy.restart,
            "quit": lazy.shutdown,
            }

    def load(self, kind: str, keys: List[str]):
        func = self.funcs[kind]
        self.keys.append(Key([keys[0]], keys[1], func()))


class CustomKeyLoader(KeyLoaderImpl):
    def load(self, kind: str, keys: List[str]):
        func = lazy.spawn(kind)
        self.keys.append(Key([keys[0]], keys[1], func))

class KeyManager:
    def __init__(self, input_keys: Keys):
        self.input_keys = input_keys
        self.output_keys: List[Callback] = []

    def load_keys(self, keys: BaseModel, loader: KeyLoader):
        for kind in keys.dict().keys():
            element = getattr(keys, kind)
            loader.load(kind, element)
        self.output_keys.extend(loader.extract())

    def __call__(self) -> List[Callback]:
        self.output_keys = []
        self.load_keys(self.input_keys.switch, SingleKeyLoader())
        self.load_keys(self.input_keys.move, DoubleKeyLoader())
        self.load_keys(self.input_keys.resize, DoubleKeyLoader())
        self.load_keys(self.input_keys.utils, UtilsKeyLoader())
        self.load_keys(self.input_keys.custom, CustomKeyLoader())
        self.load_keys(self.input_keys.stop, StopKeyLoader())
        return self.output_keys

class GroupsKeysLoader(KeyLoaderImpl):
    def load(self, kind: str, keys: List[str], group: Group):
        key = kind[-1]
        self.keys.extend([
            Key([keys[0]], key, lazy.group[group.name].toscreen()),
            Key(
                [keys[0], keys[1]],
                key,
                lazy.window.togroup(group.name, switch_group=True)
                )
            ])

class GroupManager:
    def __init__(self, input_keys: Keys, groups: List[Group]):
        self.input_keys = input_keys
        self.groups = groups
        self.output_keys: List[Callback] = []

    def load_keys(self, keys: BaseModel, groups: List[Group]):
        loader = GroupsKeysLoader()
        for group, kind in zip(groups, keys.dict().keys()):
            element = getattr(keys, kind)
            loader.load(kind, element, group)
        self.output_keys.extend(loader.extract())

    def __call__(self) -> List[Callback]:
        self.output_keys = []
        self.load_keys(self.input_keys.keygroups, self.groups)
        return self.output_keys

class MouseKeyLoader(KeyLoaderImpl):
    funcs = {
            "set_position_floating": [
                lazy.window.set_position_floating, lazy.window.get_position
                ],
            "set_size_floating": [
                lazy.window.set_size_floating, lazy.window.get_size
                ]
            }
    def load(self, kind: str, keys: List[str]):
        func = self.funcs[kind]
        self.keys.append(Drag([keys[0]], keys[1], func[0](), start=func[1]()))

class MouseManager:
    def __init__(self, input_keys: Keys):
        self.input_keys = input_keys
        self.output_keys: List[Callback] = []

    def load_keys(self, keys: BaseModel):
        loader = MouseKeyLoader()
        for kind in keys.dict().keys():
            element = getattr(keys, kind)
            loader.load(kind, element)
        self.output_keys.extend(loader.extract())

    def __call__(self) -> List[Callback]:
        self.output_keys = []
        self.load_keys(self.input_keys.keymouse)
        return self.output_keys
