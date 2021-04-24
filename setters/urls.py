"""setters URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls.static import static
from setters import settings


from walkapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('add/', views.add_walk, name='add_walk'),
    path('top/', views.top, name='top'),
    path('random/', views.rand_shuffle, name='random'),
    path('show/<int:walk_id>/', views.show_walk, name='show_trail'),
    path('signin/', views.login_view, name='signin'),
    path('signout/', views.logout_view, name='signout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('signup/', views.add_user, name='signup'),
    path('vote/<int:walk_id>/', views.vote, name='vote'),
    path('search_answer/', views.show_answer, name='search_answer'),
    path('profile/new_pass/', views.change_password, name='change_password'),
    path('signin/res_pass/', views.reset_password, name='reset_password'),
    path('delete/<int:walk_id>/', views.delete_walk, name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
#    urlpatterns += [
#        url(r'^media/(?P<path>.*)$',
#        serve,
#        {'document_root': settings.MEDIA_ROOT, }),
#    ]
