from dataclasses import dataclass, _MISSING_TYPE
from typing import List, Optional

@dataclass
class Item:
    name: str
    item_type: str
    default_value: int
    life_time: int = None


def extract_item(cls):
    class_vars = cls.__annotations__
    class_fields = cls.__dataclass_fields__
    items = [ Item
        (
            key, 
            class_vars[key].__name__ if hasattr(class_vars[key], '__name__')
            else str(class_vars[key])
                .replace('__main__.', '')
                .replace('typing.', ''),
            class_fields[key].default[0] 
            if isinstance(class_fields[key].default, tuple) 
            else class_fields[key].default if not isinstance(class_fields[key].default, _MISSING_TYPE) else None,
            class_fields[key].default[1] 
            if isinstance(class_fields[key].default, tuple) 
            else None
        ) for key in class_fields
    ]
    return items
    

if __name__ == '__main__':
    @dataclass
    class Template:
        attr0: str
        attr1: str = (1, 1)
        attr2: List[str] = ('a', 1)
        attr3: Optional[str] = 'a'
        attr4: Optional[List[str]] = 'a'
    items = extract_item(Template)
    print(items)
