from django.urls import path, include

urlpatterns = [
    path('api/money/', include('money.api.urls'), name='money_api'),
]
