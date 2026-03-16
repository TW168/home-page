from django.urls import path

from .views import freight_cpb_boxplot_api, presentation_home

urlpatterns = [
    path("", presentation_home, name="presentation-home"),
    path("api/freight-cpb-boxplot/", freight_cpb_boxplot_api, name="freight-cpb-boxplot"),
]
