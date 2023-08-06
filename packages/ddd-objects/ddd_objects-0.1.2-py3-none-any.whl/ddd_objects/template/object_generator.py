from email.policy import default
import os, sys
from dataclasses import dataclass
from typing import List, Optional
try:
    from .base import extract_item
except ImportError:
    sys.path.append(os.getcwd())
    from base import extract_item

gen_class_name = [
    'DOGenerator',
    'EntityGenerator',
    'ValueObjectGenerator',
    'ConverterGenerator'
]

def var_to_value_type(do_name):
    upper_list = ['id']
    parts = do_name.split('_')
    parts = [p.upper() if p in upper_list else p for p in parts ]
    parts = [p.capitalize() if not p.isupper() else p for p in parts]
    return ''.join(parts)

class DOGenerator:
    @staticmethod
    def gen(classes, save_fn='do_temp.py'):
        classes = [c for c in classes if c.__name__ not in gen_class_name]
        with open(save_fn, 'w') as f:
            f.write('from typing import List, Union')
            f.write('\n')
            f.write('from dataclasses import dataclass')
            f.write('\n')
            f.write('from ddd_objects.infrastructure.do import BaseDO')
            f.write('\n')
            f.write('NoneType=type(None)')
            f.write('\n\n')
        with open(save_fn, 'a') as f:
            for c in classes:
                items = extract_item(c)
                class_name = f'{c.__name__}DO'
                block = DOGenerator.__gen_do_class_block(class_name, items)
                f.write(block)
                f.write('\n')

    @staticmethod
    def __gen_do_class_block(class_name, items):
        def to_str(value):
            return f'"{value}"' if isinstance(value, str) else f'{value}'
        strip1 = [
            f'    {item.name}: {item.item_type}={to_str(item.default_value)}' if item.default_value is not None 
            else f'    {item.name}: {item.item_type}'
            for item in items
        ]
        strip1 = '\n'.join(strip1)
        block = f"""
@dataclass
class {class_name}(BaseDO):
{strip1}
        """
        return block


class ValueObjectGenerator:
    @staticmethod
    def gen(classes, save_fn='value_obj_temp.py'):

        classes = [c for c in classes if c.__name__ not in gen_class_name]
        all_items = [extract_item(c) for c in classes]
        items = []
        cache = {}
        for _items in all_items:
            for item in _items:
                if item.name in cache:
                    continue
                else:
                    cache[item.name] = 0
                items.append(item)
        
        with open(save_fn, 'w') as f:
            f.write('from ddd_objects.domain.entity import ExpiredValueObject')
            f.write('\n\n')
            for item in items:
                f.write(ValueObjectGenerator.__gen_var_class_block(item))
            f.write('\n')

    @staticmethod
    def __gen_var_class_block(item):
        block = f"""
class {var_to_value_type(item.name)}(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, {item.life_time})
"""
        return block


class EntityGenerator:

    @staticmethod
    def gen(classes, save_fn='entity_temp.py'):
        classes = [c for c in classes if c.__name__ not in gen_class_name]
        all_items = [extract_item(c) for c in classes]

        with open(save_fn, 'w') as f:
            f.write('from typing import List')
            f.write('\n')
            f.write('from ddd_objects.domain.entity import Entity')
            f.write('\n')
            f.write('from .value_obj import (')
            f.write('\n')
            cache = {}
            for items in all_items:
                for item in items:
                    if item.name in cache:
                        continue
                    else:
                        cache[item.name] = 0
                    f.write(f'    {var_to_value_type(item.name)},')
                    f.write('\n')
            f.write(')')
            f.write('\n\n')
            for items, c in zip(all_items, classes):
                block = EntityGenerator.__gen_do_class_block(c.__name__, items)
                f.write(block)
                f.write('\n')

    @staticmethod
    def __gen_do_class_block(class_name, items):
        strip1 = [f'        {item.name}: {var_to_value_type(item.name)}' for item in items]
        strip2 = [f'        self.{item.name}={item.name}' for item in items]
        strip1 = ',\n'.join(strip1)
        strip2 = '\n'.join(strip2)
        block = f"""
class {class_name}(Entity):
    def __init__(
        self,
{strip1}
    ):
{strip2}
              
        """
        return block

class ConverterGenerator:

    @staticmethod
    def gen(classes, save_fn='converter_temp.py'):
        classes = [c for c in classes if c.__name__ not in gen_class_name]
        all_items = [extract_item(c) for c in classes]
        entity_names = [c.__name__ for c in classes]

        with open(save_fn, 'w') as f:
            f.write('from typing import List')
            f.write('\n')
            f.write('from ddd_objects.infrastructure.converter import Converter')
            f.write('\n')
            f.write('from ddd_objects.domain.entity import (')
            f.write('\n')
            for entity_name in entity_names:
                f.write(f'    {entity_name},')
                f.write('\n')
            f.write(')')
            f.write('\n')
            f.write('from ddd_objects.infrastructure.do import (')
            f.write('\n')
            for entity_name in entity_names:
                f.write(f'    {entity_name}DO,')
                f.write('\n')
            f.write(')')
            f.write('\n')
            f.write('from .value_obj import (')
            f.write('\n')
            cache = {}
            for items in all_items:
                for item in items:
                    if item.name in cache:
                        continue
                    else:
                        cache[item.name] = 0
                    f.write(f'    {var_to_value_type(item.name)},')
                    f.write('\n')
            f.write(')')
            f.write('\n\n')
            for items, c in zip(all_items, classes):
                block = ConverterGenerator.__gen_do_class_block(c.__name__, items)
                f.write(block)
                f.write('\n')

    @staticmethod
    def __gen_do_class_block(class_name, items):
        strip1 = [
            f'            {item.name} = {var_to_value_type(item.name)}(do.{item.name})' 
            for item in items
        ]
        strip2 = [f'            {item.name} = x.{item.name}.get_value()' for item in items]
        strip1 = ',\n'.join(strip1)
        strip2 = ',\n'.join(strip2)
        block = f"""
class {class_name}Converter(Converter):
    def to_entity(self, do: {class_name}DO):
        return {class_name}(
{strip1}
        )
    def to_do(self, x: {class_name}):
        return {class_name}DO(
{strip2}
        )
              
        """
        return block


if __name__ == '__main__':
    @dataclass
    class Template:
        attr0: str
        attr1: str = (1, 1)
        attr2: List[str] = ('a', 1)
        attr3: Optional[str] = 'a'
        attr4: Optional[List[str]] = 'a'
    # DOGenerator.gen([Template])
    # ValueObjectGenerator.gen([Template])
    # EntityGenerator.gen([Template])
    ConverterGenerator.gen([Template])