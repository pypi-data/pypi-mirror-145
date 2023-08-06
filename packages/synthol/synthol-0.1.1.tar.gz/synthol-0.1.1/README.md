# Synthol

Juice up your dependencies 💉

## Introduction

`synthol` is a lightweight, asynchronous framework for [dependency
injection](https://en.wikipedia.org/wiki/Dependency_injection) in Python 3. It
populates a typed constructor with instances of all of its non-primitive
arguments. To do this, it first discovers all of the classes contained in some
packages, and then tracks down implementations for each class and instantiates
them.

The advantage of using this framework is that a developer can define a
strongly-typed constructor for a class without concerning themselves with where
and how the class and its dependencies should be instantiated. This reduces the
overhead (in boilerplate, time, etc.) associated with using the [composite
pattern](https://en.wikipedia.org/wiki/Composite_pattern) and decouples
interface implementations. 

Synthol is useful for highly modular applications. Some motivating use cases
might be as follows:

- A microservices-based application, where there may be a large number of
  clients and services that need to interact with other services. As an
  alternative to each service/client creating a specific instance of its
  dependencies (resulting in tight coupling between service implementations) or
  repetitive, factory-like boilerplate, each client/service simply defines what
  type of services it relies on in its constructor, and the injector manages
  creating and providing instances of these to each constructor.
- An application that has some "registration" procedure for implementations of
  an interface. There are multiple ways to accomplish this, possibly requiring
  a "register" call for every implementation. Using the dependency injector
  requires very little extra code: simply a call to `discover` modules where
  implementations live and a call to `get_instance` of a list of interface
  implementations. This scales favorably when more implementations are added or
  more interfaces need their implementations registered.
- Mocking services for unit testing is easy with the dependency injector, since
  service instantiation for an application is already centralized in the
  injector. Binding the mocked interfaces to mock implementations is all that
  is required, and then an application using the injector will get the mocked
  implementations where the interface is needed.
- Simplifying a big block of code which sets up a context for an application by
  instantiating several required services. 

## Install

Install Synthol with `pip`.

```
python3 -m pip install synthol
```

## Zoo Example

"Foo" is overdone, so let's create a `Zoo`:

```python
from synthol import DependencyInjector
from animal_api import CatInterface, DogInterface, KangarooInterface
import animal_api_implementations

class Zoo:
    def __init__(
        self,
        cat: CatInterface,
        dog: DogInterface,
        kangaroo: KangarooInterface,
    ):
        self.cat = cat
        self.dog = dog
        self.kangaroo = kangaroo


injector = DependencyInjector()
injector.discover(animal_api_implementations)

...
# In an async function...
    zoo = await injector.get_instance(Zoo)
```

This discovers all classes defined in `animal_api_implementations` when
`discover` is called. Then, when `get_instance` is called, the injector
searches those known classes for implementations of `CatInterface`,
`DogInterface`, and `KangarooInterface`. Let's assume it finds one of each.
Then each of those concrete implementations will be instantiated. But what if
there are multiple possible implementations?

## Binding a Specific Implementation for an Interface

In order to guarantee our zoo has the most amazing animals, we can be more
specific about what kind of animals to include. For example, rather than
accepting any old `CatInterface` implementation, let's specify that we want a
[Chimera](https://en.wikipedia.org/wiki/Chimera_%28mythology%29).
 
```python
from synthol import DependencyInjector
from animal_api import CatInterface, DogInterface, KangarooInterface
import animal_api_implementations
from animal_api_implementations import Chimera

class Zoo:
    def __init__(
        self,
        cat: CatInterface,
        dog: DogInterface,
        kangaroo: KangarooInterface,
    ):
        self.cat = cat
        self.dog = dog
        self.kangaroo = kangaroo
        

injector = DependencyInjector()
injector.discover(animal_api_implementations)
injector.bind_factory(Chimera)
```

The addition of the `bind_factory` specifies that the `Chimera` class should be
used when any of the interfaces it implements (`CatInterface`) are required.
Notice that this required no change to our `Zoo` class; all we touched was the
setup for the injector.

See the [Providers](#providers) section for details on the different ways to
bind implementations (or instances) for interfaces.

### Recursive Instantiation

Peeking at the source code for `Chimera`, we see that `Chimera` itself has some
dependencies:

```python
from example_api import CatInterface, GoatInterface, SnakeInterface

class Chimera(CatInterface):
    def __init__(
        self,
        goat: GoatInterface,
        snake: SnakeInterface,
    ):
        self.goat = goat
        self.snake = snake

    ...
```

Since a `Chimera` has the body and head of a lion, with a second head of a goat
on its back, and whose tail is the head and body of a snake, it is only logical
that it requires instances of `GoatInterface` and `SnakeInterface` (explaining
the use of composition over inheritance in this case is left as an exercise for
the reader).

The injector will find implementations of each one and instantiate objects to
pass to the `Chimera` constructor so that an instance of `Chimera` can be
passed to the `Zoo` constructor. This would be true even if we did not
specifically tell the injector to use `Chimera`; that is, the injector will
search for implementations for any interfaces required by whichever
implementations need to be instantiated for the top level `get_instances`.

### List Types

So far, the zoo has exactly one instance of each of the interfaces discovered.
But what if we (naturally) want some more variety and want to set up a whole
exhibit of all known types of cats? The framework lets us do this easily:   

```python
from synthol import DependencyInjector
from animal_api import CatInterface, DogInterface, KangarooInterface
import animal_api_implementations
from typing import List

class Zoo:
    def __init__(
        self,
        cats: List[CatInterface],
        dog: DogInterface,
        kangaroo: KangarooInterface,
    ):
        self.cats = cats
        self.dog = dog
        self.kangaroo = kangaroo


injector = DependencyInjector()
injector.discover(animal_api_implementations)

...
# In an async function...
    zoo = await injector.get_instance(Zoo)
```

Now, rather than looking for exactly one implementation of `CatInterface`, the
injector will collect all implementations, create an instance for each one, and
pass all of these to the constructor as a list.

The dependency injector *only* understands `typing.List` for this
functionality! For example, typing `cats` with `Set[CatInterface]` will raise
an error.

### Union Types

Let's now imagine that we aren't able to actually find an implementation for
`KangarooInterface` (kangaroos are rather rare, after all). We can make the
constructor more lenient about what animal becomes part of our zoo:

```python
from synthol import DependencyInjector
from animal_api import CatInterface, DogInterface, KangarooInterface, RabbitInterface
import animal_api_implementations
from typing import Union

class Zoo:
    def __init__(
        self,
        cats: List[CatInterface],
        dog: DogInterface,
        kangaroo: Union[KangarooInterface, RabbitInterface],
    ):
        self.cats = cats
        self.dog = dog
        self.kangaroo = kangaroo


injector = DependencyInjector()
injector.discover(animal_api_implementations)

...
# In an async function...
    zoo = await injector.get_instance(Zoo)
```

The dependency injector will now search not only for implementations of
`KangarooInterface` but also for implementations of `RabbitInterface`. It only
needs to find one implementation, which will be instantiated and passed to the
constructor.

This behavior is useful when the possible types for an argument may not have a
common class ancestor.

The dependency injector *only* understands `typing.Union` for this
functionality!

### Optional Types

Alternatively, we could say the kangaroo is entirely optional:

```python
from synthol import DependencyInjector
from animal_api import CatInterface, DogInterface, KangarooInterface
import animal_api_implementations
from typing import Optional

class Zoo:
    def __init__(
        self,
        cats: List[CatInterface],
        dog: DogInterface,
        kangaroo: Optional[KangarooInterface],
    ):
        self.cats = cats
        self.dog = dog
        self.kangaroo = kangaroo


injector = DependencyInjector()
injector.discover(animal_api_implementations)

...
# In an async function...
    zoo = await injector.get_instance(Zoo)
```

In this case, if no implementation for `KangarooInterface` is found, then
`None` will be passed to the `Zoo` constructor.

The dependency injector *only* understands `typing.Optional` for this
functionality!

## Singletons

The `get_instance` method has an optional boolean argument, `existing_instance`
(which defaults to `False`). If this argument is `True`, and if a valid
instance for the given interface has already been provided, the instance will
be re-used and returned a second time. This is useful for implementing the
[singleton pattern](https://en.wikipedia.org/wiki/Singleton_pattern). If this
argument is set to `False`, a unique instance of each interface will created
and provided every time the interface is requested.

## Providers

Providers (inheriting from `AbstractInstanceProvider`) handle the creation of
new instances when they are requested. Each provider can provide instances of
one or more interfaces, and may depend on getting instances of other
interfaces. 

It is uncommon for a user to have to interact with any providers directly. The
`DependencyInjector` exposes three methods that offer some control over the
injector's providers: `bind_instance`, `bind_factory`, and `bind`.

Note that each of these methods binds a _provider_ for one or more interfaces.
The provider supplies an instance of an interface, and is unrelated to the
`existing_instance` argument to `get_instance`. Once a provider has supplied an
instance of an interface, if `existing_instance` is True, that instance will be
used, and the provider will not be asked for that interface again. If
`existing_instance` is False, the provider will be asked for a new instance
each time. However, the provider is allowed to return the same object for
multiple queries. Using this machinery, there are multiple ways to implement
the singleton pattern.

### `bind_instance`

`bind_instance` allows the user to directly bind an object, such that any
request for an instance of that type returns this object. For example:

```python
# Skipping imports
# [ ... ]

class A:
    pass

class B(A):
    pass

class C(B):
    pass

class D(C):
    pass

# Skipping injector setup
# [ ... ]

c_singleton_instance = C()
injector.bind_instance(c_singleton_instance)

# In async function:
# [ ... ]
    await injector.get_instance(C)  # returns c_singleton_instance
    await injector.get_instance(B)  # returns c_singleton_instance
    await injector.get_instance(A)  # returns c_singleton_instance
    await injector.get_instance(D)  # returns new instance of D
```

### `bind_factory`

`bind_factory` allows the user to bind a `Callable` (or `AsyncCallable`)
object, which returns an instance of the desired interface `T` when an instance
of `T` is required.

`T` is determined by the type of the callable which is passed to
`bind_factory`. If the callable is a function, `T` is the return type of the
function. If the callable is a class, `T` is that class itself. `bind_factory`
also accepts arbitrary keyword arguments, which will be passed to the factory
each time it is called.

Pseudocode usage example:

```python
class A:
    def __init__(self, x: int):
        ...

injector.bind_factory(A, x=5)

# always calls A with x set to 5
await injector.get_instance(A)

global_ticker = 0
def create_a_instance() -> A:
    global global_ticker
    return A(global_ticker)
injector.bind_factory(A, create_a_instance)

# returns A with x set to whatever the value of global_ticker is at time of instantiation
await injector.get_instance(A)


class B:
    def __init__(self, a_instance: A, other_arg: int):
        ...

injector.bind_factory(B, other_arg=10)

# returns an instance of B with other_arg set to 10, and a_instance populated by dependency
injection
await injector.get_instance(B)
```

### `bind`

`bind` is the most open-ended option. The user can create their own instance of
an `AbstractInstanceProvider` (or one of its implementations) and bind it here.
That abstract class has abstract methods like `get_dependencies` and
`create_instance` which must be defined. It would be very unusual to need to
call `bind` directly like this, as `bind_instance` or `bind_factory` should be
sufficient for most use cases. Because it is such an unlikely case, creating a
provider this way is out of scope for this README.

`bind_factory` and `bind_instance` are implemented using `bind`.

## Contributing & Project Status

We will happily accept merge requests for code and/or documentation from the
community!

Red Balloon uses Synthol both internally, and as a dependency of other open
source projects. As such, the project is actively maintained, even if there are
no recent commits. 

### Running tests
The following commands will run the tests:
```sh
make develop  # or make install-test
make test
```
