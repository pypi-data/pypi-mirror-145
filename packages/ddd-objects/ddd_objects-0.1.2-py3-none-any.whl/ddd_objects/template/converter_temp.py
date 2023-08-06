from typing import List
from ddd_objects.infrastructure.converter import Converter
from ddd_objects.domain.entity import (
    Template,
)
from ddd_objects.infrastructure.do import (
    TemplateDO,
)
from .value_obj import (
    Attr0,
    Attr1,
    Attr2,
    Attr3,
    Attr4,
)


class TemplateConverter(Converter):
    def to_entity(self, do: TemplateDO):
        return Template(
            attr0 = Attr0(do.attr0),
            attr1 = Attr1(do.attr1),
            attr2 = Attr2(do.attr2),
            attr3 = Attr3(do.attr3),
            attr4 = Attr4(do.attr4)
        )
    def to_do(self, x: Template):
        return TemplateDO(
            attr0 = x.attr0.get_value(),
            attr1 = x.attr1.get_value(),
            attr2 = x.attr2.get_value(),
            attr3 = x.attr3.get_value(),
            attr4 = x.attr4.get_value()
        )
              
        
