# Backend-agnostic Array Type adapted from SQLAlchemy docs
# http://docs.sqlalchemy.org/en/rel_0_8/core/types.html#backend-agnostic-guid-type
import pickle
from sqlalchemy.types import TypeDecorator, Text
from sqlalchemy.dialects.postgresql import ARRAY

class Array(TypeDecorator):
    """Platform-independent Array type.

    Uses Postgresql's ARRAY type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = Type

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(ARRAY)
        else:
            return dialect.type_descriptor(Text)

    def process_bind_param(self, value, dialect):
        if value is None or dialect.name == 'postgresql':
            return value
        else:
            return pickle.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None or dialect.name == 'postgresql':
            return value
        else:
            return pickle.loads(value)
            

