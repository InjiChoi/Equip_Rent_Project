from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from managements import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('managements.urls')),
    path('equipment/', include('equipments.urls')),
    path('student/', include('students.urls')),
    path('users/', include('users.urls')),
    path('graphs/', include('graphs.urls')),
    path('receivecode.html/', views.receivecode, name='receivecode'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)