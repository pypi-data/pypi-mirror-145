from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

import db.views as views
from db import string_models

urlpatterns = [
    path(
        f'{model.lower().replace("_table", "")}/',
        getattr(views, f'{model}APIView').as_view(),
        name=model.lower()
    )
    for model in string_models
] + [
    path("login/", views.LoginView.as_view()),
    path("access-token/", views.AccessTokenView.as_view()),
    path("save-log/", views.SaveLogView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)