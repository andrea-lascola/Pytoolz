[![Build Status](https://travis-ci.com/andrea-lascola/Pytoolz.svg?branch=master)](https://travis-ci.com/andrea-lascola/Pytoolz)
[![PyPI version](https://badge.fury.io/py/pytoolz.svg)](https://badge.fury.io/py/pytoolz)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/2441/badge)](https://bestpractices.coreinfrastructure.org/projects/2441)

# Pytoolz 🚀

Module containing some python utilities/abstractions
python >= 3.7 compatible

## Prerequisites
    python >= 3.7

## Installing
    pip install pytoolz

## Sections

* [Functional](#functional) λ
* [Data Structures](#data-structures) 📂
* [Cache](#cache) 🚀
* [Design](#design) 🏛
* [Logs](#logs) 📖
* [Multiprocess](#multiprocess) 👯
* [Serialization](#serialization) 🤖

#### Functional

A set of utilities oriented to functional programming.

##### compose(f1: Callable, f2: Callable) -> Callable
Compose two functions: return the fn composition of the two

```python
from pytoolz.functional import compose

if __name__ == "__main__":
    f = compose(lambda x: x * 2,
                lambda x: x * 3)
    f(10)
    # 60
```

##### pipe(functions: List[Callable], obj)
Recursively apply a list of morphism to an input value

```python
from pytoolz.functional import pipe

if __name__ == "__main__":
    pipe([lambda x: x * 3,
          lambda x: x * 2,
          lambda x: x / 3], 10)
    # 20.0
```

##### flat_map(fn: Callable, collection: Iterable)
Apply the input function to every element in iterable and flatten the result list
s
```python
from pytoolz.functional import flat_map

if __name__ == "__main__":
    flat_map(lambda x: [x, x], [1, 2, 3])
    # [1, 1, 2, 2, 3, 3]
    flat_map(lambda x: (x, x), [1, 2, 3])
    # [1, 1, 2, 2, 3, 3]
```

##### iflat_map(fn: Callable, collection: Iterable)
Apply the input function to every element in iterable and flatten the result list **lazily**

```python
from pytoolz.functional import iflat_map

if __name__ == "__main__":
    iflat_map(lambda x: [x, x], [1, 2, 3])
    # [1, 1, 2, 2, 3, 3]
    iflat_map(lambda x: (x, x), [1, 2, 3])
    # [1, 1, 2, 2, 3, 3]
```


##### for_each(fn: Callable, collection: Iterable)
Create side effect applying the input function for every element in iterable

```python
from pytoolz.functional import iflat_map

if __name__ == "__main__":
    iflat_map(lambda x: [x, x], [1, 2, 3])
    # [1, 1, 2, 2, 3, 3]
    iflat_map(lambda x: (x, x), [1, 2, 3])
    # [1, 1, 2, 2, 3, 3]
```



##### Stream(iterable: Iterable) -> Stream
[Experiment] Emulate the Java Stream API to create pipelines of transformations unsing function composition

```python
from pytoolz.functional import Stream

if __name__ == "__main__":
    Stream([1, 2, 3]).map(lambda x: x * 3).to_list()
    # [3, 6, 9]
    Stream([1, 2, 3]).sum().to_int()
    # 6
    Stream([1, 2, 3]).map(lambda x: x * 3).filter(lambda x: x >= 6).to_tuple()
    # (6, 9)
    Stream(["a", "b", "c"]).map(lambda x: x + "a").to_set() == {'aa', 'ba', 'ca'}
    # True
    Stream([1, 4, 3]) \
        .map(lambda x: x + 3) \
        .map(lambda x: x * x) \
        .filter(lambda x: x > 3) \
        .sum() \
        .to_float()
    # 101.0

    #Alternative constructor
    Stream.of([1, 2, 3], [
        (Stream.map, lambda x: x * 3),
        (Stream.map, lambda x: x * 3)
    ]).to_list()
    # [9, 18, 27]
```

#### Serialization

Serialization and deSerialization of objects:
different engine are built-in: Json/Pickle/Dict

```python
from pytoolz.serialization import Dict, Json, Pickle

if __name__ == "__main__":
    original = '{"users": ["bob", "foo", "bar"], "companies": {}}'

    data = Json(original).deserialize()
    print(type(data))
    # '<class 'dict'>'

    string_data = Json(data).serialize()
    print(type(string_data))
    # '<class 'str'>'
```

#### Data structures
Utilities related to data structures (missing data structures or customization of existing ones) 

##### LinkedList 

```python
from pytooolz.ds import LinkedList, Node

if __name__ == "__main__":
    ll = LinkedList()
    ll.add(Node(3))
    ll.add(Node(4))
    ll.add(Node(5))
    ll.add(Node(6))
    print(ll)
    #$ LinkedList(head=Node(value=6, next=Node(value=5, next=Node(value=4, next=Node(value=3, next=None)))))
```

##### DoublyLinkedList

TODO complete

#### Cache
Utilities related to **caching**. Different backend will be implemented:
ex:
* Redis
* Memcache
* LRU in-memory
* Filesystem

```python
from pytooolz.cache import memoize # memoize decorator
from pytooolz.cache import FileEngine # Disk cache engine
from pytooolz.cache import InMemoryEngine # LRU in memory engine
from pytooolz.cache import MemcachedEngine # Memcache engine
from pytooolz.cache import RedisEngine # Redis engine

if __name__ == "__main__":
    @memoize(InMemoryEngine(limit=10, expiration=10))
    def fn(*args):
        return args


    fn(1, 2, 3, 4, 5) # fn evaluated
    fn(1, 2, 3, 4, 5) # got from cache
    fn(1, 2, 3, 4, 5) # got from cache
    fn(1, 2, 3, 4, 5) # got from cache
```


#### Design
Utilities related to application design
**Singleton decorator** - Examples:
```python
from pytooolz.design import singleton

if __name__ == "__main__":
    @singleton.singleton
    class MyClass:
        pass

    assert id(MyClass()) == id(MyClass())
```

#### Logs
**log decorators**
    - multiple backends


## Authors

* **Andrea La Scola** - *Initial work* - [PurpleBooth](https://github.com/andrea-lascola)
