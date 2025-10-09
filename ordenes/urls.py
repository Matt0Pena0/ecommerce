from django.urls import path

from .views.listar import OrdenListView
from .views.detalle import (
    OrdenDetailView,
    OrdenTxtView,
    OrdenExcelView,
    OrdenTxtCopyView,
)


app_name = "ordenes"

urlpatterns = [
    path("listar/", OrdenListView.as_view(), name="listar"),
    path("detalle/<int:pk>/", OrdenDetailView.as_view(), name="detalle"),
    path('exportar/txt/<int:pk>/', OrdenTxtView.as_view(), name='exportar_txt'),
    path('exportar/copiar/<int:pk>/', OrdenTxtCopyView.as_view(), name='exportar_copia'),
    path('exportar/excel/<int:pk>/', OrdenExcelView.as_view(), name='exportar_excel'),
    # path('exportar/pdf/<int:pk>/', OrdenPDFView.as_view(), name='exportar_pdf'),
]