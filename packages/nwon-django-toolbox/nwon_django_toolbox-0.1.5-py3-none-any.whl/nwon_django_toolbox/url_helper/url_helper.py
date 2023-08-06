from typing import Type, Union

from django.db.models import Model
from django.urls import reverse
from django.utils.html import format_html

from nwon_django_toolbox.typings.model_type import ModelType


def detail_url_for_model(
    model: ModelType[Model], primary_key: Union[str, int, None] = None
):
    primary_key = primary_key if primary_key else model.id
    return detail_url_for_model_class(model.__class__, primary_key)


def detail_url_for_model_class(model: Type[Model], primary_key: Union[str, int]):
    view_name = _base_name_from_model_class(model) + "-detail"

    url = reverse(
        viewname=view_name,
        kwargs={"pk": primary_key},
    )
    return url


def list_url_for_model_class(model_class: Type[Model]):
    return reverse(_base_name_from_model_class(model_class) + "-list")


def list_url_for_model(model: ModelType[Model]):
    return list_url_for_model_class(model.__class__)


def formatted_django_admin_link(
    model: ModelType[Model], application: str = "tamoc"
) -> str:
    url = django_admin_link_for_model(model, application)
    return format_html("<a href='{url}'>{text}</a>", url=url, text=model.__str__())


def django_admin_link_for_model(
    model: ModelType[Model], application: str = "tamoc"
) -> str:
    return reverse(
        "admin:%s_%s_change" % (application, _base_name_from_model(model)),
        args=(model.pk,),
    )


def _base_name_from_model_class(model_class: Type[Model]) -> str:
    return model_class.__name__.lower()


def _base_name_from_model(model: ModelType[Model]) -> str:
    return _base_name_from_model_class(model.__class__)


__all__ = [
    "detail_url_for_model",
    "detail_url_for_model_class",
    "list_url_for_model_class",
    "list_url_for_model",
    "formatted_django_admin_link",
    "django_admin_link_for_model",
]
