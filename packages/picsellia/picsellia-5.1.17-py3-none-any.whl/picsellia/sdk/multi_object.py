
from typing import TypeVar, Generic, List, Union
from picsellia import exceptions as exceptions
from picsellia.sdk.dao import Dao
from picsellia.sdk.connexion import Connexion
from beartype import beartype

from picsellia.bcolors import bcolors
import warnings
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning
warnings.filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)

T = TypeVar('T', bound=Dao)

class MultiObject(Generic[T]):

    @beartype
    def __init__(self, connexion: Connexion, items: List[T]) -> None:
        self._connexion = connexion

        if items == []:
            raise exceptions.NoDataError("A MultiObject can't be empty")

        self.items : list[T] = items
    
    @property
    def connexion(self) -> Connexion:
        return self._connexion

    @beartype
    def __str__(self,) -> str:
        return "{}MultiObject{} object, size: {}".format(bcolors.GREEN, bcolors.ENDC, len(self))

    @beartype
    def __getitem__(self, key) -> None:
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __add__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __sub__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __mul__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __truediv__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __floordiv__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __mod__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __pow__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __rshift__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __lshift__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __and__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __or__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __xor__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __lt__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __gt__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __le__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __ge__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")

    @beartype
    def __eq__(self, other):
        if isinstance(other, List):
            if len(other) != len(self.items):
                return False

            for item in self.items:
                if item not in other:
                    return False

        if isinstance(other, MultiObject):
            if self.connexion != other.connexion or len(self.items) != len(other.items):
                return False

            for item in self.items:
                if item not in other.items:
                    return False
        else:
            return False

        return True

    @beartype
    def __iadd__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")
    
    @beartype
    def __isub__(self, other):
        raise NotImplementedError("Not implementend. Please contact support")


    @beartype
    def __len__(self) -> int:
        return len(self.items)

    @beartype
    def assert_enough_items(self) -> None:
        if len(self.items) < 2:
            raise exceptions.NoDataError("You can't remove from this list the last item. A MultiObject can't be empty")

    @beartype
    def assert_same_connexion(self, other: Union['MultiObject', Dao]) -> None:
        if self.connexion != other.connexion:
            raise exceptions.PicselliaError('Objects that you manipulate does not come from the same client.')

    @beartype
    def __delitem__(self, i: int) -> None:
        self.assert_enough_items()
        del self.items[i]

    @beartype
    def __setitem__(self, i: int, v: T) -> None:
        self.assert_same_connexion(v)
        self.items[i] = v

    @beartype
    def append(self, x: T) -> None:
        self.assert_same_connexion(x)
        self.items.append(x)

    @beartype
    def extend(self, objects: Union[T, 'MultiObject[T]', List[T]]) -> None:
        if isinstance(objects, Dao):
            self.assert_same_connexion(objects)
        elif isinstance(objects, MultiObject) or isinstance(objects, List):
            for x in objects:
                self.assert_same_connexion(x)
        else:
            raise TypeError(objects)
        self.items.extend(objects)

    @beartype
    def insert(self, i: int, x: T) -> None:
        self.assert_same_connexion(x)
        self.items.insert(i, x)

    @beartype
    def remove(self, x: T) -> None:
        self.assert_enough_items()
        self.items.remove(x)

    @beartype
    def pop(self, i: int = None) -> T:
        self.assert_enough_items()
        if i:
            return self.items.pop(i)
        else:
            return self.items.pop()

    @beartype
    def clear(self) -> None:    
        raise exceptions.NoDataError("You can't clear a MultiObject.")

    @beartype
    def index(self, x: T, start: int = None, end: int = None) -> int:
        if start:
            if end:
                return self.items.index(x, start, end)
            else:
                return self.items.index(x, start)
        else:
            return self.items.index(x)

    @beartype
    def count(self, x: T) -> int:
        return self.items.count(x)

    @beartype
    def sort(self, key = None, reverse = False) -> None:    
        self.items.sort(key=key, reverse=reverse)

    @beartype
    def reverse(self) -> None:    
        self.items.reverse()

    @beartype
    def copy(self) -> 'MultiObject':
        raise NotImplementedError("Not implementend. Please contact support")


