from typing import Optional
from time import time

try:
    from sqlalchemy.ext.declarative import declarative_base
    SQLALCHEMY_ENV = True
except:
    SQLALCHEMY_ENV = False

if SQLALCHEMY_ENV:
    SqlalchemyBase = declarative_base()

class BaseDO:
    def to_json(self):
        return vars(self)

    def from_json(self):
        raise NotImplementedError

class ExpiredDO(BaseDO):
    def __init__(self, life_time:Optional[int]=None) -> None:
        self.life_time = life_time
        if self.life_time is None:
            self.expired_time = None
        else:
            self.expired_time = time()+self.life_time

    @property
    def is_expired(self):
        if self.expired_time is None:
            return False
        else:
            return self.expired_time>time()        

class DOGenerator:

    @staticmethod
    def gen(classes, save_fn='do_.py'):
        classes = [c[1] for c in classes 
            if c[0]!='DOGenerator' 
            and c[0]!='EntityGenerator'
            and c[0]!='ValueObjectGenerator'
            and c[0]!='ConverterGenerator'
        ]
        with open(save_fn, 'w') as f:
            f.write('from typing import List')
            f.write('\n')
            f.write('from ddd_objects.infrastructure.do import ExpiredDO')
            f.write('\n\n')
        with open(save_fn, 'a') as f:
            for c in classes:
                class_name = c.__name__
                class_vars = c.__annotations__
                life_time = c.life_time
                del class_vars['life_time']
                class_vars = {
                    key: class_vars[key].__name__ 
                    if hasattr(class_vars[key], '__name__') 
                    else str(class_vars[key]).replace('__main__.', '').split('.')[-1]
                    for key in class_vars
                }
                block = DOGenerator.__gen_do_class_block(class_name, class_vars, life_time)
                f.write(block)
                f.write('\n')


    @staticmethod
    def __gen_do_class_block(class_name, class_vars, life_time):
        strip1 = [f'        {key}: {class_vars[key]}' for key in class_vars]
        strip2 = [f'        self.{key}={key}' for key in class_vars]
        strip1 = ',\n'.join(strip1)
        strip2 = '\n'.join(strip2)
        block = f"""
class {class_name}(ExpiredDO):
    def __init__(
        self,
{strip1}
    ):
{strip2}
        super().__init__(life_time={life_time})
              
        """
        return block

class EntityGenerator:

    @staticmethod
    def gen(classes, save_fn='entity_.py'):
        classes = [c[1] for c in classes 
            if c[0]!='DOGenerator' 
            and c[0]!='EntityGenerator'
            and c[0]!='ValueObjectGenerator'
            and c[0]!='ConverterGenerator'
        ]
        type_dict = {}
        entity_types = [c.__name__ for c in classes]
        for c in classes:
            class_vars = c.__annotations__
            del class_vars['life_time']
            var_types = class_vars.keys()
            var_types = [var_to_entity_type(t) for t in var_types]
            var_types = [v for v in var_types if v not in entity_types ]
            for t in var_types:
                type_dict[t] = 0
        with open(save_fn, 'w') as f:
            f.write('from typing import List')
            f.write('\n')
            f.write('from ddd_objects.domain.entity import Entity')
            f.write('\n')
            f.write('from .value_obj import (')
            f.write('\n')
            for t in type_dict:
                f.write(f'    {t},')
                f.write('\n')
            f.write(')')
            f.write('\n\n')
        with open(save_fn, 'a') as f:
            for c in classes:
                class_name = c.__name__
                class_vars = c.__annotations__
                class_vars = {
                    key: class_vars[key].__name__ 
                    if hasattr(class_vars[key], '__name__') 
                    else str(class_vars[key]).replace('__main__.', '').split('.')[-1]
                    for key in class_vars
                }
                block = EntityGenerator.__gen_do_class_block(class_name, class_vars)
                f.write(block)
                f.write('\n')

    @staticmethod
    def __gen_do_class_block(class_name, class_vars):
        strip1 = [f'        {key}: {var_to_entity_type(key)}' for key in class_vars]
        strip2 = [f'        self.{key}={key}' for key in class_vars]
        strip1 = ',\n'.join(strip1)
        strip2 = '\n'.join(strip2)
        block = f"""
class {class_name[:-2]}(Entity):
    def __init__(
        self,
{strip1}
    ):
{strip2}
              
        """
        return block

class ValueObjectGenerator:

    @staticmethod
    def gen(classes, save_fn='value_obj_.py'):
        classes = [c[1] for c in classes 
            if c[0]!='DOGenerator' 
            and c[0]!='EntityGenerator'
            and c[0]!='ValueObjectGenerator'
            and c[0]!='ConverterGenerator'
        ]
        type_dict = {}
        entity_types = [c.__name__[:-2] for c in classes]
        for c in classes:
            class_vars = c.__annotations__
            del class_vars['life_time']
            var_types = class_vars.keys()
            var_types = [var_to_entity_type(t) for t in var_types]
            var_types = [v for v in var_types if v not in entity_types ]
            for t in var_types:
                type_dict[t] = 0
        with open(save_fn, 'w') as f:
            f.write('from ddd_objects.domain.entity import ValueObject')
            f.write('\n\n')
            for var_type in type_dict:
                f.write(ValueObjectGenerator.__gen_var_class_block(var_type))
            f.write('\n')

    @staticmethod
    def __gen_var_class_block(var_type):
        block = f"""
class {var_type}(ValueObject):
    pass
              
"""
        return block

class ConverterGenerator:

    @staticmethod
    def gen(classes, save_fn='converter_.py'):
        classes = [c[1] for c in classes 
            if c[0]!='DOGenerator' 
            and c[0]!='EntityGenerator'
            and c[0]!='ValueObjectGenerator'
            and c[0]!='ConverterGenerator'
        ]
        type_dict = {}
        do_types = [c.__name__ for c in classes]
        entity_types = [c.__name__[:-2] for c in classes]
        for c in classes:
            class_vars = c.__annotations__
            del class_vars['life_time']
            var_types = class_vars.keys()
            var_types = [var_to_entity_type(t) for t in var_types]
            var_types = [v for v in var_types if v not in entity_types ]
            for t in var_types:
                type_dict[t] = 0
        with open(save_fn, 'w') as f:
            f.write('from typing import List')
            f.write('\n')
            f.write('from ddd_objects.infrastructure.converter import Converter')
            f.write('\n')
            f.write('from ..domain.value_obj import (')
            f.write('\n')
            for t in type_dict:
                f.write(f'    {t},')
                f.write('\n')
            f.write(')')
            f.write('\n')
            f.write('from ..domain.entity import (')
            f.write('\n')
            for e in entity_types:
                f.write(f'    {e},')
                f.write('\n')
            f.write(')')
            f.write('\n')
            f.write('from .do import (')
            f.write('\n')
            for d in do_types:
                f.write(f'    {d},')
                f.write('\n')
            f.write(')')
            f.write('\n\n')
        with open(save_fn, 'a') as f:
            for c in classes:
                class_name = c.__name__
                class_vars = c.__annotations__
                class_vars = {
                    key: class_vars[key].__name__ 
                    if hasattr(class_vars[key], '__name__') 
                    else str(class_vars[key]).replace('__main__.', '').split('.')[-1]
                    for key in class_vars
                }
                block = ConverterGenerator.__gen_do_class_block(class_name, class_vars)
                f.write(block)
                f.write('\n')

    

    @staticmethod
    def __gen_do_class_block(class_name, class_vars):
        strip1 = [
            f'            {key}={var_to_entity_type(key)}(do.{key})' 
            for key in class_vars
        ]
        strip2 = [
            f'            {key}=x.{key}.get_value()' for key in class_vars
        ]
        strip1 = ',\n'.join(strip1)
        strip2 = ',\n'.join(strip2)
        block = f"""
class {class_name[:-2]}Converter(Converter):
    def to_entity(self, do: {class_name}):
        return {class_name[:-2]}(
{strip1}
        )
    def to_do(self, x: {class_name[:-2]}):
        return {class_name}(
{strip2}
        )
              
        """
        return block

def var_to_entity_type(do_name):
    parts = do_name.split('_')
    parts = [p.capitalize() if not p.isupper() else p for p in parts]
    return ''.join(parts)