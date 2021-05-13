import uuid
from typing import List, Dict

from dateutil.parser import parse
from sqlalchemy import (Column, String, DateTime, Boolean, inspect, MetaData)
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# metadata = Base.metadata
# metadata.naming_convention = convention
# Base.metadata = metadata

metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)
UUID4_LENGTH = 32
ISO_8601 = '%Y-%m-%dT%H:%M:%S.%fZ'

def generate_uuid():
    return str(uuid.uuid4())


class BaseModel(Base):
    __abstract__ = True
    __table_args__ = {'extend_existing': True}

    id = Column(String(UUID4_LENGTH), primary_key=True, default=generate_uuid)
    _created = Column(DateTime, index=True)
    _updated = Column(DateTime, )
    _deleted = Column(Boolean, server_default="false")

    extras: List[str] = []

    def serialize(self, includes: List[Dict] = None, excludes: List[str] = None, relations: List[str] = None) -> dict:
        serialized_model = dict()
        for column in inspect(self).mapper.column_attrs:
            column_value = getattr(self, column.key)
            if column_value and isinstance(column.columns[0].type, DateTime):
                column_value = parse(str(column_value)).strftime(ISO_8601)
            serialized_model[column.key] = column_value

        includes = includes or []
        excludes = excludes or []
        relations = relations or []

        for include in includes:
            serialized_model.update(include)

        if excludes:
            for key in excludes:
                if key in serialized_model.keys():
                    del serialized_model[key]

        for relation_name in relations:
            relation = getattr(self, relation_name)
            if isinstance(relation, list):
                serialized_model[relation_name] = [item.serialize() for item in relation]
            elif isinstance(relation, BaseModel):
                serialized_model[relation_name] = relation.serialize()
            else:
                serialized_model[relation_name] = None

        for extra in self.extras:
            extra_value = getattr(self, extra, None)
            if extra_value is None:
                continue
            serialized_model[extra] = extra_value

        return serialized_model

    def set_extra(self, extra_key: str, extra_value):
        if extra_key not in [column.key for column in inspect(self).mapper.column_attrs]:
            setattr(self, extra_key, extra_value)
            self.extras.append(extra_key)
