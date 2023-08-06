from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # jwt implementation
    # https://simpleisbetterthancomplex.com/tutorial/2018/12/19/how-to-use-jwt-authentication-with-django-rest-framework.html
    path('api-token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('api/', include('db.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)