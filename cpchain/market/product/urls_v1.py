from django.conf.urls import url, include
from rest_framework import routers

from cpchain.market.product.es_views import ESProductView
from cpchain.market.product.views import *

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^my_tag/subscribe/$', ProductTagSubscribeAPIView.as_view(), name='product_tag_subscribe'),
    url(r'^my_tag/unsubscribe/$', ProductTagUnsubscribeAPIView.as_view(), name='product_tag_unsubscribe'),
    url(r'^my_tag/search/$', MyTagSearchAPIView.as_view(), name='my_tag_search'),
    url(r'^my_tag/product/search/$', MyTaggedProductSearchAPIView.as_view(), name='my_tagged_product_search'),

    url(r'^my_seller/subscribe/$', ProductSellerSubscribeAPIView.as_view(), name='product_seller_subscribe'),
    url(r'^my_seller/unsubscribe/$', ProductSellerUnsubscribeAPIView.as_view(), name='product_seller_unsubscribe'),
    url(r'^my_seller/search/$', MyFollowingSellerSearchAPIView.as_view(), name='product_mytag_search'),
    url(r'^my_seller_product/search/$', MyFollowingSellerProductSearchAPIView.as_view(), name='product_seller_search'),

    url(r'^my_product/search/$', MyProductSearchAPIViewSet.as_view(), name='my_product_search'),
    url(r'^my_product_paged/search/$', MyProductPagedSearchAPIViewSet.as_view(), name='my_product_paged_search'),

    url(r'^product/show/$', ProductShowAPIViewSet.as_view(), name='product_show'),
    url(r'^product/hide/$', ProductHideAPIViewSet.as_view(), name='product_hide'),
    url(r'^product/publish/$', ProductPublishAPIViewSet.as_view(), name='product_publish'),
    url(r'^product/search/$', ProductSearchAPIViewSet.as_view(), name='product_search'),
    url(r'^product_paged/search/$', ProductPagedSearchAPIViewSet.as_view(), name='product_paged_search'),

    url(r'^es_product/search/$', ESProductView.as_view(), name='es_product_search'),

    url(r'^recommend_product/list/$', RecommendProductsAPIView.as_view(), name='recommend_products'),
    url(r'^sales_quantity/add/$', ProductSalesQuantityAddAPIView.as_view(), name='product_sales_quantity_add'),

]