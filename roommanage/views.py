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
from roommanage.models import Classroom, bookClassroom
import pandas as pd
import collections
from django.core.mail import send_mail

# Create your views here.
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
        ts = ts.floor(freq='1H')
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
                ['iftesamulohi@gmail.com'],
                    )
            send_mail(
                subject,
                'Hi I am '+name+' .\n'+message,
                'iftesamulohi@gmail.com',
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

        


class Dashboard(LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('login')
    template_name = "roommanage/dashboard.html"
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

    
    

