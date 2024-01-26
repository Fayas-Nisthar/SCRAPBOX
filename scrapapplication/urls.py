"""
URL configuration for scrapboxapplication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from scrapboxapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("signup/",views.RegisterView.as_view(),name="signup"),
    path("",views.SigninView.as_view(),name="signin"),
    path("scrap/add/",views.ProductAddView.as_view(),name="productadd"),
    path("signout/",views.SignoutView.as_view(),name="signout"),
    path("scrapbox",views.ProductListView.as_view(),name="home"),
    path("scrap/<int:pk>/details/",views.ProductDetailsView.as_view(),name="product-details"),
    path("scrap/<int:pk>/bids/",views.BidListView.as_view(),name="bid-list"),
    path("scrap/<int:pk>/bids/update/",views.BidUpdateView.as_view(),name="bid-update"),
    path("scrap/ads/",views.MyProductsView.as_view(),name="my-ads"),
    path("scrap/<int:pk>/addfav/",views.WishlistAddView.as_view(),name="add-fav"),
    path("scrap/fav/",views.FavAdsView.as_view(),name="fav"),
    path("scrap/<int:pk>/update/",views.ProductUpdateView.as_view(),name="prdct-update"),
    path("scrap/<int:pk>/delete/",views.ProductDeleteView.as_view(),name="prdct-delete"),
    path("scrap/<int:pk>/profile/",views.ProfileUpdateView.as_view(),name="profile-update"),
    path("scrap/<int:pk>/profile/details/",views.ProfileDetailView.as_view(),name="profile-detail"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
