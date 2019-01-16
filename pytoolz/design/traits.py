import abc
import functools
from functools import partial


class Trait:
    __metaclass__ = abc.ABCMeta

    def __not_available(self):
        raise Exception("Cannot Instantiate a Trait Operator")

    def __call__(self, *args, **kwargs):
        self.__not_available()

    def __init__(self):
        self.__not_available()


def extendable(clazz):
    get_instance = clazz.__new__

    @functools.wraps(clazz)
    def new(_type, *_, **__):
        instance = get_instance(_type)

        def with_trait(cls, _instance, trait: Trait):
            for prop, value in trait.__dict__.items():
                if not "__" == prop[:2]:
                    if isinstance(value, staticmethod):
                        _instance.__dict__[prop] = value
                    elif isinstance(value, classmethod):
                        _instance.__dict__[prop] = value
                    elif callable(value) and 'self' in value.__code__.co_varnames[:1]:
                        _instance.__dict__[prop] = partial(value, _instance)
                    else:
                        _instance.__dict__[prop] = value
            return _instance

        instance.__dict__["with_trait"] = partial(with_trait, clazz, instance)
        return instance

    clazz.__new__ = new
    return clazz


if __name__ == "__main__":
    class UserRenderHtml(Trait):
        def render(self):
            print("""
                <h1>{0!s}</h1>
                <p>{1!s}</p>
            """.format(self.name, self.surname))


    class UserRenderText(Trait):
        def render(self):
            print(self.name, self.surname)


    @extendable
    class User:
        def __init__(self, name, surname):
            self.name = name
            self.surname = surname


    usr = User("Andrea", "La Scola").with_trait(UserRenderHtml)
    print(usr.render())
