from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name='todoapp'

urlpatterns = [
    path('',views.home, name='home'),
    path('index',views.lhome, name='lhome'),
    
    # Delete Paths
    path('<int:todo_id>/delete', views.delete, name='delete'),
    path('<int:cat_id>/deletecategory', views.deletecategory, name='deletecategory'),

    #Update Paths
    path('<int:todo_id>/update', views.update, name='update'),

    # Add Paths
    path('add', views.add, name='add'),
    path('addcategory', views.addcategory, name='addcategory'),
    path('permisions', views.permisions, name='permisions'),
    path('addpermision/', views.addpermision, name='addpermision'),

    path('filtertodos/', views.filtertodos, name='filtertodos'),
    path('filtertodosdate/', views.filtertodosdate, name='filtertodosdate'),

    #User Registration url
    path('login', views.userloginurl, name='userloginurl'),
    path('register', views.register, name='register'),
    path('logind', views.logind, name='logind'),
    path('logout', views.logout_view, name='logout'),
]