from django.urls import path
from .views import *

app_name = 'shortner'

urlpatterns = [
    path('<int:pk>/edit/', ShortURLEditView.as_view(), name='url_edit'),
    path('<int:pk>/delete/', ShortURLDeleteView.as_view(), name='url_delete'),
    path('list/', ShortURLListView.as_view(), name='url_list'),
    path('', URLShortenerView.as_view(), name="home"),
    path('<str:short_part>/', URLShortenerView.as_view(), name='redirect_short_url'),
    
]

