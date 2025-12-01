from django.urls import path
from .views import (
    HomeListView, ContactsTemplateView,
    ProductListView, ProductDetailView,
    ProductCreateView, ProductUpdateView, ProductDeleteView,
    unpublish_product, publish_product, toggle_publish_status  # 🆕 импортируем новые функции
)

app_name = 'catalog'  # ✅ должно быть

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    # 🆕 URL для управления публикацией
    path('product/<int:pk>/unpublish/', unpublish_product, name='product_unpublish'),
    path('product/<int:pk>/publish/', publish_product, name='product_publish'),
    path('product/<int:pk>/toggle-publish/', toggle_publish_status, name='product_toggle_publish'),
]