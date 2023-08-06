from django.urls import path, include
from .views import AdminSingleDeleteView
app_name = 'softdelete'

urlpatterns = [
    path('<str:app_label>/<str:model>/<str:pk>/', AdminSingleDeleteView.as_view(), name='single-delete'),
    # path('<str:app_label>/<str:model>/<str:pks>/', AdminBulkDeleteView.as_view(), name='bulk-delete'),

]