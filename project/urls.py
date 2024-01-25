"""
URL configuration for project project.

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
from projectapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminmain/',views.adminmain,name='adminmain'),
    path('usermain/',views.usermain,name='usermain'),
    path('index/',views.home,name='indexpage'),
    path('adminindex/',views.adminhome,name='adminindex'),
    path('admin-login/',views.adminlogin,name='adminlogin'),
    path('user-login/', views.userlogin, name="userlogin"),
    path('admin-logout/',views.adminlogout,name="adminlogout"),
    path('user-logout/',views.userlogout,name="userlogout"),
    path('admin-register/',views.adminregister,name='adminregister'),
    path('user-register/',views.userregister,name='userregister'),
    path('search/',views.searchbox, name='search'),
    path('adminhome/',views.EmpListView, name='adminhome'),
    path('empdetail/<slug:slug>/',views.EmpDetailView, name='empdetail'),
    path('editemp/<slug:slug>/',views.editemp,name='editemp'),
    path('editempadmin/<slug:slug>/',views.editempadmin,name='editempadmin'),
    path('profile/', views.userprofile, name="profile"),
    path('update-attendance/<slug:slug>/', views.attendanceup, name='update_attendance'),
    path('showattendance/',views.showattendance,name='showattendance'),
    path('attendance/', views.attendancelist, name='attendance_list'),
    path('attendanceupadmin/<slug:slug>/',views.attendanceupadmin,name='attendanceupadmin'),
    path('deletepofile/<slug:slug>/',views.deleteprofile,name='deleteprofile'),
    path('update/<int:id>',views.update,name='update'),
    path('show/<slug:slug>/', views.adminshow, name="showattendance1"),
    path('adminattendancelist/',views.adminattendancelist,name='adminattendancelist'),
    path('updt/',views.updt, name="updt")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)