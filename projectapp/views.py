from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse
from projectapp.models import employee, hr,attendance, head
from django.db.models import Q
from datetime import datetime
from django.urls import reverse



# Create your views here.
def EmpListView(request):
    hrs = request.session['hr']
    empobj = hr.objects.get(Email = hrs)
    employ = employee.objects.all()
    return render(request,'home.html',{'hr':empobj,'employ':employ})

def EmpDetailView(request,slug):
    hrs = request.session['hr']
    empobj = hr.objects.get(Email = hrs)
    employ = employee.objects.get(slug = slug)
    return render(request,'empdetail.html',{'hr':empobj,'empdetail':employ})

def Editemp(request,slug):
    if request.method =='GET':
        hrs = request.session['hr']
        empobj = hr.objects.get(Email = hrs)
        employ = employee.objects.get(slug = slug)
        return render(request,'editform.html',{'user':empobj,'empdetail':employ})
    elif request.method =='POST':
        hrs = request.session['hr']
        empobj = hr.objects.get(Email = hrs)
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

#navbar for hrpage
def hrmain(request):
    return render(request,'hrmain.html')

#after hr login
def hrhome(request):
    if 'hr' in request.session:
        hrs= request.session.get('hr')
        hrobj= hr.objects.get(Email=hrs)
        return render(request, 'hrindex.html', {'hr': hrobj,'empdetail': hrobj})
    
#delete user profile from hr
def deleteprofile(request,slug):
    if 'hr' in request.session:
        hrs= request.session.get('hr')
        hrobj= hr.objects.get(Email=hrs)
        obj = employee.objects.get(slug=slug)
        obj.delete()
        return redirect('../../hrhome/')
    
#hr edit user details   
def editemphr(request,slug):
    if request.method =='GET':
        hrs= request.session['hr']
        hrobj= hr.objects.get(Email=hrs)
        employ = employee.objects.get(slug = slug)
        return render(request,'editformhrend.html',{'hr':hrobj,'empdetail':employ})
    elif request.method =='POST':
        hrs= request.session['hr']
        hrobj= hr.objects.get(Email=hrs)
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
        return render(request,'empdetail.html',{'hr':hrobj,'empdetail':employ})
    
#update user attendance from hr end
# def update(request,id):
#     if request.method == 'GET':
#         if 'hr' in request.session:
#             hrs= request.session.get('hr')
#             hrobj= hr.objects.get(Email=hrs)
#             obj = attendance.objects.get(id=id)
#             return render(request,'showattendance.html',{'hr':hrobj,'obj':obj})
#     elif request.method =='POST':
#         if 'hr' in request.session:
#             hr= request.session.get('hr')
#             hrobj= hr.objects.get(Email=hr)
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

#hr login
def hrlogin(request):
    if request.method=="GET":
        return render(request,"hrlogin.html")
    elif request.method=="POST":
        hrs = request.POST['email']
        hrobj = hr.objects.filter(Email = hrs)
        if hrobj:
            hrobj = hr.objects.get(Email=request.POST.get("email"))
            passfe = request.POST.get("password")
            flag = check_password(passfe,hrobj.Password)

            if flag:
                request.session['hr'] = request.POST.get('email')
                return redirect("../chatgpt/")
            else:
                error_message = "Wrong credentials !! Oops try again :("
                return render(request,'hrlogin.html',{'msg':error_message})

        else:
            error_message = "No User found"
            return render(request,'hrlogin.html',{'msg':error_message})

#hr logout       
def hrlogout(request):
    request.session['email'] = ''
    return redirect('../hr-login/')  

#hrregister
def hrregister(request):
    if request.method=="GET":
        return render(request,"hrregister.html")
    elif request.method=="POST":
        name = request.POST.get("fname")
        designation = request.POST.get("designation")
        department = request.POST.get("department")
        email =request.POST.get("email")
        password= request.POST.get("password")
        passw = make_password(password)
        hrobj = hr(Name=name, Designation=designation,Department=department,Email=email,Password=passw)
        hrobj.save()

        return HttpResponse("hr registered Successfully")

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
        if request.POST.get('designation') == 'Section Head':
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
            slugobj = name+'-'+designation
            head1 = 'HR'
            empobj = head(Name=name, Photo = photo,Gender=gender,Designation=designation,Department=department, City = city,DOB = dateofbirth,Address=address,State=state,Pincode=pincode,PhoneNo=phoneno,Email=email,Password=passw,slug=slugobj)
            empobj.save()
            emp1obj = employee(Name=name, Photo = photo,Gender=gender,Designation=designation,Department=department, Head=head1, City = city,DOB = dateofbirth,Address=address,State=state,Pincode=pincode,PhoneNo=phoneno,Email=email,Password=passw,slug=slugobj)
            emp1obj.save()
        else:
            name = request.POST.get("fname")
            photo =request.FILES.get("photo")
            gender = request.POST.get("gender")
            dateofbirth = request.POST.get("DOB")
            address = request.POST.get("address")
            state = request.POST.get("state")
            city = request.POST.get("city")
            designation = request.POST.get("designation")
            department = request.POST.get("department")
            head1 = request.POST.get("head")
            pincode = request.POST.get("pincode")
            phoneno = request.POST.get("phone")
            email =request.POST.get("email")
            password= request.POST.get("password")
            passw = make_password(password)
            slugobj = name+'-'+designation
            empobj = employee(Name=name, Photo = photo,Gender=gender,Designation=designation,Department=department, Head=head1, City = city,DOB = dateofbirth,Address=address,State=state,Pincode=pincode,PhoneNo=phoneno,Email=email,Password=passw,slug=slugobj)
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

#attendance list at hr end   
def hrattendancelist(request):
    if request.method== "POST":
        hrs= request.session['hr']
        empobj= hr.objects.get(Email=hrs)
        obj = request.POST['eid']
        print(obj)
        attobj = attendance.objects.filter(employee_id= obj)
        selected_month = request.POST.get('monthFilter')

        if selected_month:
            attobj = attendance.objects.filter(date__month=selected_month,employee_id=obj)
        else:
            attobj = attendance.objects.filter(employee_id=obj)

        return render(request,'showattendancehr.html',{'hr':empobj,'attobj':attobj})

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
        
#attendance update form at hr end   
def attendanceuphr(request,slug):
    if request.method == 'GET':
        current_time = datetime.now().strftime('%H:%M:%S')   
        print(current_time)
        hrs= request.session['hr']
        hrobj= hr.objects.get(Email=hrs)
        empobj = employee.objects.get(slug = slug)
        print(empobj.id)
        return render(request,'attendanceuphr.html',{'hr':hrobj,'empobj1':empobj,'time':current_time})
    elif request.method == 'POST':
        hrs= request.session['hr']
        hrobj= hr.objects.get(Email=hrs)
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


def hrshow(request, slug):
    if request.method == 'GET':
        hrs= request.session.get('hr')
        hrobj= hr.objects.get(Email=hrs)
        emp= employee.objects.get(slug= slug)
        atobj= attendance.objects.filter(employee_id=emp.id)
        return render(request, 'showattendancehr.html',{'hr':hrobj,'empobj':emp,'attobj':atobj})
    elif request.method== "POST":
        hrs= request.session['hr']
        empobj= hr.objects.get(Email=hrs)
        obj = request.POST['eid']
        print(obj)
        attobj = attendance.objects.filter(employee_id= obj)
        selected_month = request.POST.get('monthFilter')

        if selected_month:
            attobj = attendance.objects.filter(date__month=selected_month,employee_id=obj)
        else:
            attobj = attendance.objects.filter(employee_id=obj)

        return render(request,'showattendancehr.html',{'hr':empobj,'attobj':attobj})

def update(request, id):
    if 'hr' in request.session:
            hrs= request.session.get('hr')
            hrobj= hr.objects.get(Email=hrs)
            obj = attendance.objects.get(id=id)
            return render(request,'update.html',{'hr':hrobj,'obj':obj})
    

# for update atndce in hr panel 
def updt(request):
    if request.method=="POST":
        hrs= request.session.get('hr')
        hrobj= hr.objects.get(Email=hrs)
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
    
def chatgpt(request):
    hrs= request.session['hr']
    hrobj= hr.objects.get(Email=hrs)
    return render(request,'chatgpt.html',{'hr':hrobj})