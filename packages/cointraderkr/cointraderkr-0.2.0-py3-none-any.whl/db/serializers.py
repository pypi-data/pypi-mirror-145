from rest_framework import serializers

import db.models as models
from db import string_models

def _meta(model_cls):
    class Meta:
        model = model_cls
        fields = '__all__'
    return Meta

for model in string_models:
    vars()[f'{model}Serializer'] = type(
        f'{model}Serializer',
        (serializers.ModelSerializer,),
        {
            'Meta': _meta(getattr(models, model))
        }
    )