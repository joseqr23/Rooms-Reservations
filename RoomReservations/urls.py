from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg import views, openapi

schema_view = views.get_schema_view(
	openapi.Info(
		title = "Rooms Reservation API",
        default_version= "v1",
        description= "API for a hotel room reservation system",
        terms_of_service= "https://www.google.com/policies/terms/",
        contact= openapi.Contact(email="jquisper2@gmail.com"),
        license= openapi.License(name="MIT"),
	),
    public= True,
    permission_classes= [permissions.AllowAny]
)


urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v1/', include("Reservations.urls")),

	re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
	re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
