from django.urls import path, include
from .views import home, ProjectCreateView, project_detail

urlpatterns = [
   path('', home, name='home'),
   path('add/', ProjectCreateView.as_view(), name='add'),
   path('<slug:project_slug>/', project_detail, name='detail')
]
