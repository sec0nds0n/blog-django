from django.urls import path, reverse_lazy
from .views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(success_url=reverse_lazy('login')), name='signup'),
]
