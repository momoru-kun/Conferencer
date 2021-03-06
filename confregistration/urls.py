from django.contrib import admin
from django.urls import path, include
from client.views import AdminPanel, Index, Quiz

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('admin', AdminPanel.as_view()),
    path('', Index.as_view()),
    path('c_<str:conf_id>', Quiz.as_view()),
    path('api/', include('api.urls'))
]
urlpatterns += staticfiles_urlpatterns()