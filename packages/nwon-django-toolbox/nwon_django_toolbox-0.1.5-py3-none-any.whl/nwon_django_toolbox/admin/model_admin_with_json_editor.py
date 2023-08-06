from django import forms
from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from nwon_django_toolbox.fields.encrypted_text_field.encrypted_text_field import (
    EncryptedTextField,
)


class ModelAdminWithJsonEditor(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


class ModelAdminWithJsonEditorReadOnly(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {
            "widget": JSONEditorWidget(options={"mode": "view", "modes": ["view"]})
        },
        EncryptedTextField: {
            "widget": forms.PasswordInput(render_value=False),
        },
    }


__all__ = ["ModelAdminWithJsonEditorReadOnly", "ModelAdminWithJsonEditor"]
