
from django.urls import path
from . import views


urlpatterns = [

    path('download/', views.FileDownloadAPIView.as_view(), name='file_download'),
    path("",views.ShowAllItemApiView.as_view()),
    path("listall/",views.ShowAllItemApiView.as_view()),
    path("grab/<int:item>",views.GrabUrlItemApiViews.as_view()),
    path("product/",views.GrabParameterItemApiView.as_view()),

]
