from invenio_records.models import RecordMetadataBase
from invenio_db import db
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils.types import JSONType


class LooseValidityBase(RecordMetadataBase):
    validace = db.Column(
        db.JSON().with_variant(
            postgresql.JSONB(none_as_null=True),
            'postgresql',
        ).with_variant(
            JSONType(),
            'sqlite',
        ).with_variant(
            JSONType(),
            'mysql',
        ),
        default=lambda: dict(),
        nullable=True
    )
