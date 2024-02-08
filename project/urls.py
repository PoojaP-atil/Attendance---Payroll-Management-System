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
    path('hrmain/',views.hrmain,name='hrmain'),
    path('usermain/',views.usermain,name='usermain'),
    path('index/',views.home,name='indexpage'),
    path('hrindex/',views.hrhome,name='hrindex'),
    path('hr-login/',views.hrlogin,name='hrlogin'),
    path('acc-login/',views.acclogin,name='acclogin'),
    path('user-login/', views.userlogin, name="userlogin"),
    path('hr-logout/',views.hrlogout,name="hrlogout"),
    path('user-logout/',views.userlogout,name="userlogout"),
    path('hr-register/',views.hrregister,name='hrregister'),
    path('user-register/',views.userregister,name='userregister'),
    path('search/',views.searchbox, name='search'),
    path('hrhome/',views.EmpListView, name='hrhome'),
    path('acchome/',views.accempview, name='acchome'),
    path('empdetail/<slug:slug>/',views.EmpDetailView, name='empdetail'),
    path('accempdetail/<slug:slug>/',views.accempview, name='accempdetail'),
    path('editemp/<slug:slug>/',views.editemp,name='editemp'),
    path('editemphr/<slug:slug>/',views.editemphr,name='editemphr'),
    path('profile/', views.userprofile, name="profile"),
    path('update-attendance/<slug:slug>/', views.attendanceup, name='update_attendance'),
    path('showattendance/',views.showattendance,name='showattendance'),
    path('attendance/', views.attendancelist, name='attendance_list'),
    path('attendanceuphr/<slug:slug>/',views.attendanceuphr,name='attendanceuphr'),
    path('deletepofile/<slug:slug>/',views.deleteprofile,name='deleteprofile'),
    path('update/<int:id>',views.update,name='update'),
    path('show/<slug:slug>/', views.hrshow, name="showattendance1"),
    path('accshow/<slug:slug>/', views.accshow, name="accshowattendance1"),
    #path('hrattendancelist/',views.hrattendancelist,name='hrattendancelist'),
    path('updt/',views.updt, name="updt"),
    path('hrheadhome/',views.hrheadhome,name='hrheadhome'),
    path('calendar/<int:year>/<int:month>/', views.month_calendar, name='month_calendar'),
    path('path/to/prev/month/<int:year>/<int:month>/', views.month_calendar, name='month_calendar'),
    path('path/to/next/month/<int:year>/<int:month>/', views.month_calendar, name='month_calendar'),
    path('calculation/',views.calculation,name='calculation'),
    path('submit_leave_request/', views.submit_leave_request, name='submit_leave_request'),
    path('calculate_payment/', views.calculation1, name='calculate_payment'),
    path('salarypayment/<str:tid>/<int:empid>/<str:month>/',views.salarypayment,name='salarypayment'),
    path('paymentdetails/', views.paymentdetails, name='paymentdetails'),
    path('invoice/',views.invoice,name='invoice')


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)