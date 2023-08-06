from rest_framework.serializers import ModelSerializer

from tamoc.utils.fields.pydantic_json_field.pydantic_json_field import PydanticJsonField
from tamoc.utils.fields.pydantic_json_field.pydantic_json_field_serializer import (
    PydanticJsonFieldSerializer,
)


class ModelSerializerWithPydantic(ModelSerializer):
    """
    REST Framework ModelSerializer including a mapping of our custom PydanticJsonField
    """

    serializer_field_mapping = {
        **ModelSerializer.serializer_field_mapping,
        **{PydanticJsonField: PydanticJsonFieldSerializer},
    }
