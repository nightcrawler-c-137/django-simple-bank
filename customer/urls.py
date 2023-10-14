from django.urls import path, include

from .views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('api-auth/', include('rest_framework.urls'))
 
]
