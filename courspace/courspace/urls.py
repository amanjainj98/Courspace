## @brief urls for the website.
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

## @brief url patterns for the website.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login_user, name='login_user'),
    url(r'^register_user/$', views.register_user, name='register_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^course/', include('course.urls', namespace='course')),
    url(r'^instructor/', include('instructor.urls', namespace='instructor')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)