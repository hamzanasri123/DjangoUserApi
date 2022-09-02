from django.urls import path

from users.models import Permission
from .views import  (PermissionAPIView, users,register,login,AuthentificatedUser,logout,RoleViewSet,UserGenericAPIView,ProfileInfoAPIView,ProfilePasswordAPIView)

urlpatterns = [

    path('users', users),
    path('register',register),
    path('login',login),
    path('logout',logout),
    path('user',AuthentificatedUser.as_view()),
    path('permissions',PermissionAPIView.as_view()),
    path('roles',RoleViewSet.as_view({
        'get':'list',
        'post':'create',
    })),
    path('roles/<str:pk>',RoleViewSet.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path('allUsers/info',ProfileInfoAPIView.as_view()),
    path('allUsers/password',ProfilePasswordAPIView.as_view()),
    path('allUsers',UserGenericAPIView.as_view()),
    path('allUsers/<str:pk>',UserGenericAPIView.as_view()),
    
]
