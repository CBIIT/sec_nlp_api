from dataclasses import dataclass, is_dataclass, field


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
    display: str
    code: str = field(default=None)
    system: str = field(default=None)

    def __post_init__(self):
        self.curate_system()
        self.remove_duplicates_from_display()
        self.remove_words_three_characters_or_less()
        self.remove_number_strings()
        self.remove_units_of_messurements()

    def curate_system(self):
        if self.system:
            self.system = self.system.split('/')[-1].upper()

    def remove_units_of_messurements(self):
        if self.display:
            # Still an issue with things like 100MG
            special_messurements = [
                'unt/ml', 'ml', '/ml', 'hr',
                'mg', 'lf'
            ]
            words = self.display.split(' ')
            self.display = ' '.join([word for word in words if word not in special_messurements ])

    def remove_number_strings(self):
        if self.display:
            words = self.display.split(' ')
            self.display = ' '.join([word for word in words if not word.isnumeric()])

    def remove_words_three_characters_or_less(self):
        if self.display:
            words = self.display.split(' ')
            self.display = ' '.join([word for word in words if len(word) > 3])

    def remove_duplicates_from_display(self):
        if self.display:
            self.display = ' '.join(dict.fromkeys(self.display.lower().split()))

@nested_dataclass
class Codes:
    coding: [Code]
    # attr_accessor :system, :code, :display

    def __post_init__(self):
        pass
