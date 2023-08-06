from typing import List, Optional, Type

import jsonref
from django.db.models.fields import Field
from pydantic.error_wrappers import ValidationError as PydanticValidationError
from pydantic.main import BaseModel
from rest_framework.serializers import JSONField

__all__ = ["PydanticJsonFieldSerializer"]


class PydanticJsonFieldSerializer(JSONField, Field):
    """
    Serializer for serializing our custom PydanticJsonField
    """

    class Meta:
        swagger_schema_fields: dict

    def __init__(
        self, *args, pydantic_models: Optional[List[Type[BaseModel]]] = None, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.pydantic_models = pydantic_models if pydantic_models else []

        print("Pydantic Field Serializer")
        print(self.field_name)
        print(kwargs)
        print(pydantic_models)
        print(
            "schema from model "
            + str(self.__schema_field_from_argument(pydantic_models))
        )

        # Set information for swagger generator drf_yasg
        PydanticJsonFieldSerializer.Meta.swagger_schema_fields = (
            self.__schema_field_from_argument(pydantic_models)
        )

    def to_representation(self, value):
        value = super().to_representation(value)

        for model in self.pydantic_models:
            try:
                if isinstance(value, dict):
                    return model.parse_obj(value).dict()
                else:
                    return model.parse_raw(value).dict()
            except PydanticValidationError:
                pass

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        for model in self.pydantic_models:
            try:
                parsed_json = model.parse_obj(data)
                return parsed_json.dict()
            except PydanticValidationError:
                pass

        self.fail("invalid")

    def __schema_field_from_pydantic(self, pydantic_model: Type[BaseModel]) -> dict:
        return jsonref.loads(pydantic_model.schema_json())

    def __schema_field_from_argument(
        self, pydantic_models: Optional[List[Type[BaseModel]]]
    ):
        return (
            self.__schema_field_from_pydantic(pydantic_models[0])
            if pydantic_models and pydantic_models.__len__() > 0
            else {}
        )
