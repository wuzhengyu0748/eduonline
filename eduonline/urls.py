"""eduonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from django.views.static import serve

import xadmin

from apps.users.views import LoginView, LogoutView, RegisterView
from eduonline.settings import MEDIA_ROOT
from apps.operation.views import IndexView

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    url(r'^media/(?P<path>.*)$', serve, {'document_root':MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve, {'document_root':STATIC_ROOT}),

    # 机构相关
    url(r'^org/', include(('apps.organizations.urls', 'organizations'), namespace='org')),
    # 用户操作相关
    url(r'^op/', include(('apps.operation.urls', 'operation'), namespace='op')),
    # 课程相关
    url(r'^course/', include(('apps.courses.urls', 'courses'), namespace='course')),
    # 用户个人中心相关
    url(r'^users/', include(('apps.users.urls', 'users'), namespace='users')),
]
