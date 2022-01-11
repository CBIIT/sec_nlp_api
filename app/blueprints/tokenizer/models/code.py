from dataclasses import dataclass, field

from dataclasses import dataclass, is_dataclass

def nested_dataclass(*args, **kwargs):

    def wrapper(check_class):

        # passing class to investigate
        check_class = dataclass(check_class, **kwargs)
        o_init = check_class.__init__

        def __init__(self, *args, **kwargs):

            for name, value in kwargs.items():
                # getting field type
                ft = check_class.__annotations__.get(name, None)
                if is_dataclass(ft) and isinstance(value, dict):
                    obj = ft(**value)
                    kwargs[name] = obj
                elif isinstance(ft, list) and is_dataclass(ft[0]):
                    objs = []
                    if value:
                        for val in value:
                            objs.append(ft[0](**val))
                        kwargs[name] = objs
                o_init(self, *args, **kwargs)
        check_class.__init__ = __init__

        return check_class

    return wrapper(args[0]) if args else wrapper

@dataclass
class Code:
    system: str
    display: str
    code: str = None

    def __post_init__(self):
        self.remove_duplicates_from_display()

    def remove_duplicates_from_display(self):
        if self.display:
            self.display = ' '.join(dict.fromkeys(self.display.lower().split()))

@nested_dataclass
class Codes:
    coding: [Code]
    # attr_accessor :system, :code, :display

    def __post_init__(self):
        pass
