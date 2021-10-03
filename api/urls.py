from django.conf.urls import url
from django.urls import path
from api import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^category/$', views.category),
    url(r'^category/([0-9]+)$', views.category),
    url(r'^subcategory/$', views.subcategory),
    url(r'^subcategory/([0-9]+)$', views.subcategory),
    url(r'^expenses/$', views.expenses),
    url(r'^expenses/([0-9]+)$', views.expenses),
    url(r'^product/$', views.product),
    url(r'^get_product/$', views.get_products),
    url(r'^get_all_products_final_admin/$', views.get_all_products_final_admin),
    url(r'^get_all_products/$', views.get_all_products),
    url(r'^get_products_search/$', views.get_products_search),
    url(r'^get_all_highlight/$', views.get_all_highlight),
    url(r'^product/([0-9]+)$', views.product),
    url(r'^stock/$', views.stock),
    url(r'^get_all_stock/$', views.get_all_stock),
    url(r'^stock/([0-9]+)$', views.stock),
    url(r'^sell/$', views.sell),
    url(r'^sell/([0-9]+)$', views.sell),
    url(r'^product/SaveFiles/$', views.SaveFile),
    url(r'^all_pending_sale/$', views.all_sells_in_process),
    url(r'^all_close_sale/$', views.all_sells_close),
    url(r'^delete_pending_sale/([0-9]+)$', views.cancel_pending_sell),
    url(r'^pending_sale/$', views.pending_sell),
    url(r'^pending_sale/([0-9]+)$', views.pending_sell),
    url(r'^client-data/$', views.client_data),
    url(r'^client-buys/$', views.buys_users),
    url(r'^all-client-data/$', views.all_client_data),
    url(r'^category/([0-9]+)$', views.client_data),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)