from typing import List, Optional, Type, Union

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

        self.__set_information_for_drf_yasg(pydantic_models)

        self.pydantic_models = pydantic_models if pydantic_models else []

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

    def __set_information_for_drf_yasg(
        self, pydantic_models: Optional[List[Type[BaseModel]]]
    ):
        """Set information for swagger generator drf_yasg"""

        if pydantic_models is None or pydantic_models.__len__() == 0:
            schema_information = {}

        elif pydantic_models.__len__() > 1:
            schema_information = {
                "anyOf": [
                    self.__schema_field_from_pydantic(model)
                    for model in pydantic_models
                ]
            }
        else:
            schema_information = self.__schema_field_from_pydantic(pydantic_models[0])

        PydanticJsonFieldSerializer.Meta.swagger_schema_fields = schema_information
