from email import message
from time import strftime
from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.models import User, auth
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date,datetime,timedelta
from django.db.models import Q
from roommanage.models import Classroom, bookClassroom,Routine
import pandas as pd
import collections
import tabula
from django.core.mail import send_mail
from django.views.generic.edit import FormView
from .forms import RoutineForm
from django.http import HttpResponse,HttpResponseRedirect
from dateutil.relativedelta import relativedelta, SA,SU,MO,TU,WE,TH,FR


import tabula

# Create your views here.
routine = Routine.objects.all()
#tabula.convert_into( "routine.pdf", "newfile.csv", output_format="csv", pages='all')
print(routine[0].routine.name)

#try code 2
from django.http import FileResponse
import os
import csv
def handle_uploaded_file(f):  
    with open('uploads/routine/pdffile.pdf', 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk) 
def classroom_update():
    Classroom.objects.all().delete()
    filepath = os.path.join('uploads/', 'routine/pdffile.pdf')
    
    a = FileResponse(open(filepath, 'rb'), content_type='application/pdf')
    tabula.convert_into( filepath, "uploads/routine/newfile.csv", output_format="csv", pages='all')
    print(filepath)
    with open("uploads/routine/newfile.csv") as file_obj:
      
    # Create reader object by passing the file 
    # object to reader method
        reader_obj = csv.reader(file_obj)
    # Iterate over each row in the csv 
    # file using reader object
    #print(reader_obj[5])
        i=0
        print("hello reader",reader_obj)
        all_rooms = []
        for row in reader_obj:
            
            if i!=0:
                all_rooms.append(row[1])

            i+=1

        all_rooms = list(dict.fromkeys(all_rooms))
        database_room = Classroom.objects.all()
        database_room2 = []
        for room in database_room:
            #print(room)
            database_room2.append(str(room))
        #print("database room",database_room2)
        dd = list(set(all_rooms)-set(database_room))
        print("not matched",dd)
        #print("all rooms",all_rooms)
        #Classroom.objects.all().delete()
        for room in all_rooms:
            Classroom.objects.create(
                title = room
            )


# book class room function
def book_class():
    bookClassroom.objects.all().delete()
    with open("uploads/routine/newfile.csv") as file_obj: 
        reader_obj2 = csv.reader(file_obj) 
        i= 0
        for row in reader_obj2:
            
            if i!=0:
                room_key = Classroom.objects.get(title=row[1]).pk
                print(room_key)
                if row[0].lower()=="satarday":
                    for x in range(24):
                        
                        bookClassroom.objects.create(
                        room = Classroom.objects.get(pk=room_key),
                        reason = row[2],
                        date = datetime.today()+relativedelta(weekday=SA(x+1)),
                        a_time = row[4].split('-')[0],
                        d_time = row[4].split('-')[1]
                            )
                        print("booked")
                elif row[0].lower()=="sunday":
                    for x in range(24):
                        
                        bookClassroom.objects.create(
                        room = Classroom.objects.get(pk=room_key),
                        reason = row[2],
                        date = datetime.today()+relativedelta(weekday=SU(x+1)),
                        a_time = row[4].split('-')[0],
                        d_time = row[4].split('-')[1]
                            )
                        print("booked")
                    print("this day",row[0])#here to start
                elif row[0].lower()=="monday":
                    for x in range(24):
                        
                        bookClassroom.objects.create(
                        room = Classroom.objects.get(pk=room_key),
                        reason = row[2],
                        date = datetime.today()+relativedelta(weekday=MO(x+1)),
                        a_time = row[4].split('-')[0],
                        d_time = row[4].split('-')[1]
                            )
                        print("booked")
                    print("this day",row[0])#here to start
                elif row[0].lower()=="tuesday":
                    for x in range(24):
                        
                        bookClassroom.objects.create(
                        room = Classroom.objects.get(pk=room_key),
                        reason = row[2],
                        date = datetime.today()+relativedelta(weekday=TU(x+1)),
                        a_time = row[4].split('-')[0],
                        d_time = row[4].split('-')[1]
                            )
                        print("booked")
                    print("this day",row[0])#here to start
                elif row[0].lower()=="wednesday":
                    for x in range(24):
                        
                        bookClassroom.objects.create(
                        room = Classroom.objects.get(pk=room_key),
                        reason = row[2],
                        date = datetime.today()+relativedelta(weekday=WE(x+1)),
                        a_time = row[4].split('-')[0],
                        d_time = row[4].split('-')[1]
                            )
                        print("booked")
                    print("this day",row[0])#here to start
                elif row[0].lower()=="thursday":
                    for x in range(24):
                        
                        bookClassroom.objects.create(
                        room = Classroom.objects.get(pk=room_key),
                        reason = row[2],
                        date = datetime.today()+relativedelta(weekday=TH(x+1)),
                        a_time = row[4].split('-')[0],
                        d_time = row[4].split('-')[1]
                            )
                        print("booked")
                    print("this day",row[0])#here to start
                elif row[0].lower()=="friday":
                    for x in range(24):
                        
                        bookClassroom.objects.create(
                        room = Classroom.objects.get(pk=room_key),
                        reason = row[2],
                        date = datetime.today()+relativedelta(weekday=FR(x+1)),
                        a_time = row[4].split('-')[0],
                        d_time = row[4].split('-')[1]
                            )
                        print("booked")
                    print("this day",row[0])#here to start

            i+=1

def timecontroller():
    time = datetime.now()
    current_time = time.strftime("%H:%M:%S")
    time_m =time.strftime("%M")
    return current_time
global allocated_time
allocated_time = "00:00:00"
global a_date
a_date = "2012-12-12"
#ts="06:00:00"
class Index(TemplateView):
    
    #tabula.convert_into( "routine.pdf", "newfile.csv", output_format="csv", pages='all')
    ts="00:00:00"
    a_date_copy = "2012-12-12"
    
    
    #template_name = "roommanage/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Classroom.objects.all()
        context['time'] =self.ts
        context['date'] = self.a_date_copy
        rooms = list(Classroom.objects.all())
        booked_rooms = list(bookClassroom.objects.filter(~Q(a_time =self.ts),date=self.a_date_copy))
        booked_roomstry = list(bookClassroom.objects.filter(Q(a_time =self.ts),date=self.a_date_copy))
        print("booked rooms see",booked_rooms)
        print("booked rooms final",booked_roomstry)
        final_booked_room = []
        final_booked_roomtry = []
        for booked_roomtry in booked_roomstry:
            thing= str(booked_roomtry)
            final_booked_roomtry.append(thing)
        for booked_room in booked_rooms:
            thing= str(booked_room)
            final_booked_room.append(thing)
        print("free name",final_booked_room)
        print("booked name",final_booked_roomtry)
        pre_empty_rooms = [i for i in final_booked_room if i not in final_booked_roomtry]
        print("result",pre_empty_rooms)
        
        empty_room = []
        for room in rooms:
            #print(room)
            for booked_room in pre_empty_rooms:
                print("rooms",room)
                print("booked rooms",booked_room)
                
                if str(room)==str(booked_room):
                    #if (bookClassroom.objects.filter(a_time =self.ts,room = booked_room.pk)):
                    empty_room.append(room)
        print("empty room without filter: ",empty_room)
        #empty_room = [item for item, count in collections.Counter(empty_room).items() if count > 1]
        empty_room  = list(dict.fromkeys(empty_room))
        print(empty_room)
        context['rooms'] = empty_room
        print("empty rooms",empty_room)
        print("converted date: ",self.a_date_copy)
        print("converted time: ",self.ts)

        return context
    def get(self,request):
        #show_pdf()
        if 'time' and 'date' in request.session:
            if request.session['time']!='' and request.session['date']!='':
                allocated_time = request.session['time']
                a_date =request.session['date']
                print("check date: ",request.session['date'])
            else:
                allocated_time = timecontroller()
                a_date = date.today().strftime("%Y-%m-%d")         
        else:
            allocated_time = timecontroller()
            a_date = date.today().strftime("%Y-%m-%d")

            
        #allocated_time = timecontroller()
        ts = pd.Timestamp(allocated_time)
        ts = ts.floor(freq='1H')+timedelta(minutes=30)
        ts = str(ts).split()
        self.ts = ts[1]
        self.a_date_copy = a_date
        #this is check code
        a = ['a','b','a','c','d','c','b']
        print([item for item, count in collections.Counter(a).items() if count > 1])
        request.session['time']=''
        request.session['date']=''
        return render(request, "roommanage/index.html",self.get_context_data())
    def post(self, request, *args, **kwargs):
        date = request.POST.get('date')
        time = request.POST.get('time')
        reason = request.POST.get('reason')
        room_key = request.POST.get('room_no')
        email = request.POST.get('user_mail')
        name = request.POST.get('user_name')
        room_title = request.POST.get('room_title')
        request.session['time'] = time
        request.session['date'] = date
        print("search date",date)
        allocated_time = request.session['time']
        a_date = request.session['date']
        if reason is not None:
            d_time = time
            print("d time",d_time)
            print("book date",date)
            d_time = datetime.strptime(d_time,'%H:%M:%S')+timedelta(hours=1)
            d_time = d_time.strftime("%H:%M:%S")
            message = "I Booked room "+room_title+" for "+date+" from "+time+" to "+d_time+"."
            subject = "Booking Confirmation"
            bookClassroom.objects.create(
                room = Classroom.objects.get(pk=room_key),
                reason = reason,
                date = date,
                a_time = time,
                d_time = d_time
            )
             # send mail
            send_mail(
                subject,
                'Hi I am '+name+' .\n'+message,
                email,
                ['joy15-13006@diu.edu.bd'],
                    )
            send_mail(
                subject,
                'Hi I am '+name+' .\n'+message,
                'joy15-13006@diu.edu.bd',
                [email],
                    )
        print("alloc: ",allocated_time)
        
        print("reason time:",time)
        print(reason)
        return redirect('index')
    
    
    
    
class LoginPage(TemplateView):
    template_name = "roommanage/pages-login.html"
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            return redirect('login')

        

'''
class Dashboard(LoginRequiredMixin,TemplateView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('pdffile')
        print(file)
        Routine.objects.create(
         routine = file
         )
        return redirect('dashboard')
    login_url = reverse_lazy('login')
    template_name = "roommanage/dashboard.html"
'''
class Dashboard(LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('login')
    template_name = "roommanage/dashboard.html"
    def get(self,request):
        return render(request,"roommanage/dashboard.html")
    def post(self,request):
        print("this is routine",request.FILES['pdffile'])
        handle_uploaded_file(request.FILES['pdffile'])
        classroom_update()
        book_class()
        return HttpResponseRedirect("dashboard")

    '''
    form_class = RoutineForm
    template_name = "roommanage/dashboard.html"
    success_url = "roommanage/index.html"
    
    def form_valid(self, form):
        review = RoutineForm(routine = form.cleaned_data['routine'])
        print("form data",routine = form.cleaned_data['routine'])
        review.save()
        return super().form_valid(form)
    
    def post(self, request):
                #print("This is update",request.FILES('routine'))
                form = RoutineForm(request.POST, request.FILES)
                
                if form.is_valid():
                    print("table clean data",form.cleaned_data["routine"])
                    instance = Routine.objects.create(routine=form.cleaned_data["routine"])
                    
                    instance.save()
                    return HttpResponseRedirect('dashboard')
                '''
        
class Bookreason(TemplateView):
    template_name = "roommanage/test.html"
    def get(self,request):
        return render(request, "roommanage/test.html",self.get_context_data())
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        return context


# def bookClassroom(request):
#     if request.method =="POST":
#         reason = request.POST.get('reason')
#         booking_date = request.POST.get('booking_date')
#         print("booking date: ",booking_date)
#         print("booking reason: ",reason)
#         return redirect('index')

    
    

