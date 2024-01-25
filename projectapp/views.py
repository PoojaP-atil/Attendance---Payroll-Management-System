from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse
from projectapp.models import employee, admins,attendance
from django.db.models import Q
from django.views.generic import ListView,DetailView
from datetime import datetime
from django.urls import reverse



# Create your views here.
def EmpListView(request):
    admin = request.session['admin']
    empobj = admins.objects.get(Email = admin)
    employ = employee.objects.all()
    return render(request,'home.html',{'admin':empobj,'employ':employ})

def EmpDetailView(request,slug):
    admin = request.session['admin']
    empobj = admins.objects.get(Email = admin)
    employ = employee.objects.get(slug = slug)
    return render(request,'empdetail.html',{'admin':empobj,'empdetail':employ})

def Editemp(request,slug):
    if request.method =='GET':
        admin = request.session['admin']
        empobj = admins.objects.get(Email = admin)
        employ = employee.objects.get(slug = slug)
        return render(request,'editform.html',{'user':empobj,'empdetail':employ})
    elif request.method =='POST':
        admin = request.session['admin']
        empobj = admins.objects.get(Email = admin)
        employ = employee.objects.get(slug = slug)
        employ.Name = request.POST.get('fname')
        employ.Address = request.POST.get('address')
        employ.City = request.POST.get('city')
        employ.State = request.POST.get('state')
        employ.Pincode = request.POST.get('pincode')
        employ.PhoneNo = request.POST.get('phone')
        employ.Email = request.POST.get('email')
        employ.Photo = request.FILES.get('photo')
        employ.save()
        return render(request,'empdetail.html',{'user':empobj,'empdetail':employ})

#navbar for adminpage
def adminmain(request):
    return render(request,'adminmain.html')

#after admin login
def adminhome(request):
    if 'admin' in request.session:
        admin= request.session.get('admin')
        admobj= admins.objects.get(Email=admin)
        return render(request, 'adminindex.html', {'admin': admobj,'empdetail': admobj})
    
#delete user profile from admin
def deleteprofile(request,slug):
    if 'admin' in request.session:
        admin= request.session.get('admin')
        admobj= admins.objects.get(Email=admin)
        obj = employee.objects.get(slug=slug)
        obj.delete()
        return redirect('../../adminhome/')
    
#admin edit user details   
def editempadmin(request,slug):
    if request.method =='GET':
        admin= request.session['admin']
        admobj= admins.objects.get(Email=admin)
        employ = employee.objects.get(slug = slug)
        return render(request,'editformadminend.html',{'admin':admobj,'empdetail':employ})
    elif request.method =='POST':
        admin= request.session['admin']
        admobj= admins.objects.get(Email=admin)
        employ = employee.objects.get(slug = slug)
        employ.Name = request.POST.get('fname')
        employ.Address = request.POST.get('address')
        employ.City = request.POST.get('city')
        employ.State = request.POST.get('state')
        employ.Pincode = request.POST.get('pincode')
        employ.PhoneNo = request.POST.get('phone')
        employ.Email = request.POST.get('email')
        employ.Photo = request.FILES.get('photo')
        employ.save()
        return render(request,'empdetail.html',{'admin':admobj,'empdetail':employ})
    
#update user attendance from admin end
# def update(request,id):
#     if request.method == 'GET':
#         if 'admin' in request.session:
#             admin= request.session.get('admin')
#             admobj= admins.objects.get(Email=admin)
#             obj = attendance.objects.get(id=id)
#             return render(request,'showattendance.html',{'admin':admobj,'obj':obj})
#     elif request.method =='POST':
#         if 'admin' in request.session:
#             admin= request.session.get('admin')
#             admobj= admins.objects.get(Email=admin)
#             dates = request.POST['date']
#             print(dates)
#             intime = request.POST.get('in_time')
#             outtime = request.POST.get('out_time')
#             statuss = request.POST.get('status')
#             upobj = attendance.objects.get(id=id)
#             upobj.date = dates
#             upobj.in_time = intime
#             upobj.out_time = outtime
#             upobj.status = statuss
#             upobj.save()
#             return redirect('../../showattendance/')

def searchbox(request):
    if request.method == "POST":
        sq= request.POST.get('search_query')
        result = employee.objects.filter(Q(Name__icontains= sq) | Q(Designation__icontains= sq) | Q(Department__icontains= sq)|Q(Gender__iexact= sq))
        return render(request, 'home.html', {'listobj':result})

#admin login
def adminlogin(request):
    if request.method=="GET":
        return render(request,"adminlogin.html")
    elif request.method=="POST":
        admin = request.POST['email']
        adm = admins.objects.filter(Email = admin)
        if adm:
            admobj = admins.objects.get(Email=request.POST.get("email"))
            passfe = request.POST.get("password")
            flag = check_password(passfe,admobj.Password)

            if flag:
                request.session['admin'] = request.POST.get('email')
                return redirect("../adminindex/")
            else:
                error_message = "Wrong credentials !! Oops try again :("
                return render(request,'adminlogin.html',{'msg':error_message})

        else:
            error_message = "No User found"
            return render(request,'adminlogin.html',{'msg':error_message})

#admin logout       
def adminlogout(request):
    request.session['email'] = ''
    return redirect('../admin-login/')  

#adminregister
def adminregister(request):
    if request.method=="GET":
        return render(request,"adminregister.html")
    elif request.method=="POST":
        name = request.POST.get("fname")
        designation = request.POST.get("designation")
        department = request.POST.get("department")
        email =request.POST.get("email")
        password= request.POST.get("password")
        passw = make_password(password)
        adminobj = admins(Name=name, Designation=designation,Department=department,Email=email,Password=passw)
        adminobj.save()

        return HttpResponse("Admin registered Successfully")

#user view

#user login
def userlogin(request):
    if request.method=="GET":
        return render(request,"userlogin.html")
    elif request.method=="POST":
        emp = employee.objects.filter(Email = request.POST.get("email"))

        if emp:
            empobj = employee.objects.get(Email=request.POST.get("email"))
            passfe = request.POST.get("password")
            flag = check_password(passfe,empobj.Password)

            if flag:
                request.session['user'] = request.POST.get('email')
                return redirect("../index/")
            else:
                error_message = "Wrong credentials !! Oops try again :("
                return render(request,'userlogin.html',{'msg':error_message})

        else:
                error_message = "No user found"
                return render(request,'userlogin.html',{'msg':error_message})

#user logout      
def userlogout(request):
    request.session['user'] = ''
    return redirect('../user-login/')  

#user regiseter
def userregister(request):
    if request.method=="GET":
        return render(request,"userregister.html")
    elif request.method=="POST":
        name = request.POST.get("fname")
        photo =request.FILES.get("photo")
        gender = request.POST.get("gender")
        dateofbirth = request.POST.get("DOB")
        address = request.POST.get("address")
        state = request.POST.get("state")
        city = request.POST.get("city")
        designation = request.POST.get("designation")
        department = request.POST.get("department")
        pincode = request.POST.get("pincode")
        phoneno = request.POST.get("phone")
        email =request.POST.get("email")
        password= request.POST.get("password")
        passw = make_password(password)
        empobj = employee(Name=name, Photo = photo,Gender=gender,Designation=designation,Department=department,City = city,DOB = dateofbirth,Address=address,State=state,Pincode=pincode,PhoneNo=phoneno,Email=email,Password=passw)
        empobj.save()

        return HttpResponse("Customer registered Successfully")
    
#navbar for userpage
def usermain(request):
    return render(request,'usermain.html')

# after userlogin   
def home(request):
    if 'user' in request.session:
        user= request.session.get('user')
        empobj= employee.objects.get(Email=user)
        return render(request, 'index.html', {'user': empobj,'empdetail': empobj})
    

#user profile
def userprofile(request):
    user= request.session['user']
    empobj= employee.objects.get(Email=user)
    return render(request, 'test1.html', {'user': empobj,'empdetail': empobj})

#user edit details    
def editemp(request,slug):
    if request.method =='GET':
        user= request.session['user']
        empobj= employee.objects.get(Email=user)
        employ = employee.objects.get(slug = slug)
        return render(request,'editform.html',{'user':empobj,'empdetail':employ})
    elif request.method =='POST':
        user= request.session['user']
        empobj= employee.objects.get(Email=user)
        employ = employee.objects.get(slug = slug)
        employ.Name = request.POST.get('fname')
        employ.Address = request.POST.get('address')
        employ.City = request.POST.get('city')
        employ.State = request.POST.get('state')
        employ.Pincode = request.POST.get('pincode')
        employ.PhoneNo = request.POST.get('phone')
        employ.Email = request.POST.get('email')
        employ.Photo = request.FILES.get('photo')
        employ.save()
        return render(request,'empdetail.html',{'user':empobj,'empdetail':employ})

#show attendance tabel to useer    
def showattendance(request):
    user= request.session['user']
    empobj= employee.objects.get(Email=user)
    attobj = attendance.objects.filter(employee=empobj.id)
    return render(request,'showattendance.html',{'user':empobj,'attobj':attobj})


# attendance list at user end
def attendancelist(request):
    if 'user' in request.session:
        user= request.session['user']
        empobj= employee.objects.get(Email=user)
        attobj = attendance.objects.filter(employee=empobj.id)
        selected_month = request.GET.get('monthFilter')

        if selected_month:
            attobj = attendance.objects.filter(date__month=selected_month,employee_id=empobj.id)
        else:
            attobj = attendance.objects.filter(employee_id=empobj.id)

        return render(request,'showattendance.html',{'user':empobj,'attobj':attobj})

#attendance list at admin end   
def adminattendancelist(request):
    if request.method== "POST":
        admin= request.session['admin']
        empobj= admins.objects.get(Email=admin)
        obj = request.POST['eid']
        print(obj)
        attobj = attendance.objects.filter(employee_id= obj)
        selected_month = request.POST.get('monthFilter')

        if selected_month:
            attobj = attendance.objects.filter(date__month=selected_month,employee_id=obj)
        else:
            attobj = attendance.objects.filter(employee_id=obj)

        return render(request,'showattendanceadmin.html',{'admin':empobj,'attobj':attobj})

# attendance marking from user end
def attendanceup(request,slug):
    if request.method == 'GET':
        current_time = datetime.now().strftime('%H:%M:%S')   
        print(current_time)
        user= request.session['user']
        empobj= employee.objects.get(Email=user)
        empobj = employee.objects.get(slug = slug)
        print(empobj.id)
        return render(request,'attendance.html',{'user':empobj,'empobj1':empobj,'time':current_time})
    elif request.method == 'POST':
        user= request.session['user']
        empobj= employee.objects.get(Email=user)
        empobj = employee.objects.get(slug = slug)
        emp = request.POST.get('empid')
        date = request.POST.get('date')
        in_time = request.POST.get('intime')
        out_time = request.POST.get('outtime')
        status = request.POST.get('status')
        attobj = attendance(date = date,in_time = in_time , out_time = out_time, employee_id=emp,status=status)
        attobj.save()
        return redirect('../../showattendance/')
        
#attendance update form at admin end   
def attendanceupadmin(request,slug):
    if request.method == 'GET':
        current_time = datetime.now().strftime('%H:%M:%S')   
        print(current_time)
        admin= request.session['admin']
        admobj= admins.objects.get(Email=admin)
        empobj = employee.objects.get(slug = slug)
        print(empobj.id)
        return render(request,'attendanceupadmin.html',{'admin':admobj,'empobj1':empobj,'time':current_time})
    elif request.method == 'POST':
        admin= request.session['admin']
        admobj= admins.objects.get(Email=admin)
        empobj = employee.objects.get(slug = slug)
        emp = request.POST.get('empid')
        date = request.POST.get('date')
        in_time = request.POST.get('intime')
        out_time = request.POST.get('outtime')
        status = request.POST.get('status')
        attobj = attendance(date = date,in_time = in_time , out_time = out_time, employee_id=emp,status=status)
        attobj.save()
        url = reverse('showattendance1', args=[empobj.slug])
        return redirect(url)


def adminshow(request, slug):
    admin= request.session.get('admin')
    admobj= admins.objects.get(Email=admin)
    emp= employee.objects.get(slug= slug)
    atobj= attendance.objects.filter(employee_id=emp.id)
    return render(request, 'showattendanceadmin.html',{'admin':admobj,'empobj':emp,'attobj':atobj})

def update(request, id):
    if 'admin' in request.session:
            admin= request.session.get('admin')
            admobj= admins.objects.get(Email=admin)
            obj = attendance.objects.get(id=id)
            return render(request,'update.html',{'admin':admobj,'obj':obj})
    

# for update atndce in admin panel 
def updt(request):
    if request.method=="POST":
        admin= request.session.get('admin')
        admobj= admins.objects.get(Email=admin)
        dates = request.POST['date']
        print(dates)
        id=  request.POST['id']
        print(id)
        intime = request.POST.get('in_time')
        outtime = request.POST.get('out_time')
        statuss = request.POST.get('status')
        upobj = attendance.objects.get(id=id)
        slugf= upobj.employee.slug
        upobj.date = dates
        upobj.in_time = intime
        upobj.out_time = outtime
        upobj.status = statuss
        upobj.save()
        url= reverse('showattendance1', args=[slugf])
        return redirect(url)