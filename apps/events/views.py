from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Venue,Event,Booking,Payment,User,Profile
from .serializers import VenueSerializer,EventSerializer,BookingSerializer,PaymentSerializer,RegisterSerializer,LoginSerializer,VerifyCodeSerializer,LogoutSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
import uuid
from django.db import transaction
import random
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
#================================================   
   
class TestAPIView(APIView):
    def get(self,request):
        return Response({'status':True})
            
#================================================          

class VenuePagination(PageNumberPagination): 
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    
#---------------

class VenueView(APIView):
    
    def get(self,request):
        queryset = Venue.objects.all()
        status = request.query_params.get('status')
        venue = request.query_params.get('venue')
        min_date = request.query_params.get('min_date')
        max_date = request.query_params.get('max_date')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')

        if status:
            queryset = queryset.filter(status=status)
        if venue:
            queryset = queryset.filter(venue_id=venue)  
        if min_date:
            queryset = queryset.filter(start_at__gte=min_date)
        if max_date:
            queryset = queryset.filter(end_at__lte=max_date)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        paginator = VenuePagination()
        result_page = paginator.paginate_queryset(queryset,request)
        serializer = VenueSerializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)
    
#---------------
        
    def post(self,request):
        if request.user.is_superuser or request.user.is_staff:
            try:
                data=request.data
                serializer = VenueSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'data':serializer.data,'message' : "عملیات ثبت موفق آمیز بود"},status = 201)
                return Response({'errors': serializer.errors,'message':'اطلاعات ورودی نامعتیر می باشد'},status = 400)
            
            except Exception as e:
                return Response({'message':'عملیات ناموفق بود!'},status= 400)
        return Response({'message': 'شما اجازه ثبت این محل برگزاری را ندارید'},status = 403)
    
#---------------
         
    def put(self,request,pk):
        if request.user.is_superuser or request.user.is_staff:
            try:
                data=request.data
                venue= Venue.objects.get(id=pk)
                serializer=VenueSerializer(venue,data=data)
            except Venue.DoesNotExist:
                return Response({'message': 'محل برگزاری پیدا نشد'},status= 404)
            
            if serializer.is_valid():
                    serializer.save()
                    return Response({'data':serializer.data,'message' : "عملیات آپدیت موفق آمیز بود"},status = 200)
            return Response({'errors': serializer.errors,'message':'اطلاعات ورودی نامعتیر می باشد'},status = 400)
            
        return Response({'message': 'شما اجازه تغییر این محل برگزاری را ندارید'},status = 403)
                
#---------------
    def patch(self,request,pk):
        if request.user.is_superuser or request.user.is_staff:   
            try:
                data=request.data
                venue= Venue.objects.get(id=pk)
                serializer=VenueSerializer(venue,data=data,partial=True)
            except Venue.DoesNotExist:
                return Response({'message': 'محل برگزاری پیدا نشد'},status = 404)
            if serializer.is_valid():
                    serializer.save()
                    return Response({'data':serializer.data,'message' : "عملیات آپدیت موفق آمیز بود"},status = 200)
            return Response({'errors': serializer.errors,'message':'اطلاعات ورودی نامعتیر می باشد'},status = 400)
            
        return Response({'message': 'شما اجازه تغییر این محل برگزاری را ندارید'},status = 403)
                
#---------------



    def delete(self,request,pk):
        if request.user.is_superuser or request.user.is_staff:   
            try:
                venue=Venue.objects.get(id=pk)
                venue.delete()
                return Response({'message': 'محل برگزاری با موفقیت حذف شد'},status = 200 )
            
            except Venue.DoesNotExist:
                return Response({'message': 'محل برگزاری پیدا نشد'},status= 404)
            
        return Response({'message': 'شما اجازه حذف این محل برگزاری را ندارید'},status= 403)
                                
                
#====================================================================================================================          

class EventPagination(PageNumberPagination): 
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    

#---------------   

class EventView(APIView):
   
    def get(self,request):
        queryset = Event.objects.all()
        paginator = EventPagination()
        result_page = paginator.paginate_queryset(queryset,request)
        serializer = EventSerializer(result_page ,many = True)
        return paginator.get_paginated_response(serializer.data)
    
    
#---------------   
    
    def post(self,request):
        if request.user.is_superuser or request.user.is_staff:
            data = request.data
            serializer = EventSerializer(data=data)
            if serializer.is_valid():
                    serializer.save(organizer = request.user)    #خودکار ست می‌شه و نیازی به ورود از طرف کاربر نداره
                    return Response({'data':serializer.data,'message' : "عملیات موفق بود"})
            return Response({'status': 400,"errors": serializer.errors ,'message':'عملیات ناموفق بود!'})
        return Response({'message': 'شما اجازه ساخت رویداد را ندارید'},status = 403)
        
#---------------    
    
    def put(self,request,pk):
        if request.user.is_superuser or request.user.is_staff:
            try:
                data = request.data
                event = Event.objects.get(id=pk)
                serializer=EventSerializer(event,data=data)
            except Event.DoesNotExist:
                return Response({'message': 'رویداد مورد نظر پیدا نشد'},status= 404)
            
            if serializer.is_valid():
                    serializer.save()
                    return Response({'data':serializer.data,'message' : "عملیات آپدیت موفق آمیز بود"},status = 200)
            return Response({'errors': serializer.errors,'message':'اطلاعات ورودی نامعتیر می باشد'},status = 400)
            
        return Response({'message': 'شما اجازه تغییر این رویداد را ندارید'},status = 403)
                
#---------------

    def patch(self,request,pk):
        if request.user.is_superuser or request.user.is_staff:
            try:
                data=request.data
                event= Event.objects.get(id=pk)
                serializer=EventSerializer(event,data=data,partial=True)
            except Event.DoesNotExist:
                return Response({'message': 'رویداد مورد نظر پیدا نشد'},status = 404)
            if serializer.is_valid():
                    serializer.save()
                    return Response({'data':serializer.data,'message' : "عملیات آپدیت موفق آمیز بود"},status = 200)
            return Response({'errors': serializer.errors,'message':'اطلاعات ورودی نامعتیر می باشد'},status = 400)
            
        return Response({'message': 'شما اجازه تغییر این رویداد را ندارید'},status = 403)
                
#---------------

    def delete(self,request,pk):
       
        if request.user.is_superuser or request.user.is_staff:
            try:
                event=Event.objects.get(id=pk)
                event.delete()
                return Response({'message': 'رویداد  با موفقیت حذف شد'},status = 200 )
            
            except Event.DoesNotExist:
                return Response({'message': 'رویداد مورد نظر پیدا نشد'},status= 404)
            
        return Response({'message': 'شما اجازه حذف این رویداد را ندارید'},status= 403)
                                
                
#====================================================================================================================  
     
class bookingPagination(PageNumberPagination): 
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
            
#---------------   
  
class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Booking.objects.filter(user=request.user) 
        paginator = bookingPagination()
        result_page = paginator.paginate_queryset(queryset,request)
        serializer = BookingSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

#---------------    
    
    def post(self, request):
        user = request.user
        event_id = request.data.get("event")
        ticket_count = int(request.data.get("ticket_count", 1))

        if ticket_count < 1:
            return Response({'message':'تعداد رزرو باید بزرگتر از صفر باشد'}, status=400)

        try:
            
            with transaction.atomic():
                event = Event.objects.select_for_update().get(id=event_id)
                if event.seats_left < ticket_count:
                    return Response({'message':'ظرفیت کافی وجود ندارد'}, status=400)

                booking = Booking.objects.create(user=user, event=event, ticket_count=ticket_count)
                event.seats_left -= ticket_count
                event.save()

                serializer = BookingSerializer(booking)
                return Response({'booking': serializer.data, 'message': "عملیات موفق بود"}, status=201)

        except Event.DoesNotExist:
                return Response({'message':'رویداد پیدا نشد'}, status=404)

#---------------      
        
    def delete(self, request, pk):
            try:
                booking = Booking.objects.get(id=pk)
                if booking.user != request.user and not request.user.is_staff:
                    return Response({'message': 'شما اجازه حذف این رزرو را ندارید'}, status=403)
                booking.event.seats_left += booking.ticket_count  # برگرداندن صندلی‌ها
                booking.event.save()
                booking.delete()
                return Response({'message': 'رزرو با موفقیت حذف شد'}, status=200)
            except Booking.DoesNotExist:
                return Response({'message': 'رزرو مورد نظر یافت نشد'}, status=404)
                                            
    
#================================================  

class PaymentView(APIView):
    
    permission_classes = [IsAuthenticated] 
    
    def get(self,request,pk):
        try:
            booking=Booking.objects.get(id=pk)
            payment=booking.payment
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=200)
        except Booking.DoesNotExist:
            return Response({'message': 'رزرو پیدا نشد'}, status=404)
        except Payment.DoesNotExist:
            return Response({'message': 'پرداختی برای این رزرو وجود ندارد'}, status=404)
    
        
    def post(self,request,pk):
        try:
            booking=Booking.objects.get(id=pk)
        except Booking.DoesNotExist:
            return Response({'message': 'رزرو پیدا نشد'}, status=404)
            
        if booking.user != request.user:
            return Response({'message': 'شما اجازه پرداخت این رزرو را ندارید'}, status=403)
        
        if hasattr(booking,'payment'):
            return Response({'message': 'پرداخت قبلاً انجام شده'}, status=400)
        
        ref = str(uuid.uuid4()).replace('-', '')[:12]
        
        payment = Payment.objects.create(booking=booking, ref=ref, status="pending")
        payment.status = "success"
        payment.save()
        serializer = PaymentSerializer(payment)
        return Response({'payment': serializer.data, 'message': 'پرداخت شبیه‌سازی شد و موفق بود'}, status=201)

        
#================================================  
  
class RegisterView(APIView):
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [] 
        return [IsAuthenticated()] 
    
    
    def get(self,request):
        if not request.user.is_staff:
             return Response({'message': 'شما اجازه دسترسی ندارید'}, status=403)

        users=User.objects.all()
        serializer=RegisterSerializer(users,many=True)
        return Response({'data':serializer.data,'message': 'لیست کاربران با موفقیت واکشی شد'},status =200)

#--------------- 
 
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data['username']
            password=serializer.validated_data['password']
            email=serializer.validated_data['email']
            user=User.objects.create_user(username=username,password=password,email=email)
            Profile.objects.create(user=user)
            return Response({'user':serializer.data,'message':'ثبت نام با موفقیت انجام شد'},status=201)
        
        return Response({'data':serializer.errors,'message':'اطلاعات ورودی صحیح نمی باشد'},status=400)
            
#---------------  

    def put(self,request,pk):
        user=User.objects.get(id=pk)
        data=request.data
        serializer=RegisterSerializer(user,data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'message':'به روز رسانی با موفقیت انجام شد'},status=201)
        return Response({'data':serializer.errors,'message':'طلاعات ورودی صحیح نمی باشد'},status=400)
    
#---------------  

    def patch(self,request,pk):
        user=User.objects.get(id=pk)
        data=request.data
        serializer=RegisterSerializer(user,data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'message':'به روز رسانی با موفقیت انجام شد'},status=201)
        return Response({'data':serializer.errors,'message':'طلاعات ورودی صحیح نمی باشد'},status=400)
    
#---------------  
    
    def delete(self,request,pk):
        try:
            user=User.objects.get(id=pk)
            user.delete()
            return Response({'message':'کاربر با موفقیت حذف شد'},status=200)
        except User.DoesNotExist:
            return Response({'message':'کاربری با این مشخصات وجود ندارد!'},status=400)
            

#================================================  

class LoginView(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(email=email)  
            except User.DoesNotExist:
                return Response({'message': 'کاربر یافت نشد'}, status=404)
            
            if user.check_password(password):
                profile = Profile.objects.get(user=user)
                code = str(random.randint(10000, 99999))
                profile.verification_code = code
                profile.save()

                # ارسال ایمیل
                send_mail('کد تایید ورود',f'کد تایید شما: {code}',settings.DEFAULT_FROM_EMAIL,[user.email],fail_silently=False,)
                
                return Response({'message': 'کد تایید به ایمیل شما ارسال شد','requires_verification': True}, status=200)
           
            return Response({'message': 'رمز عبور اشتباه است'}, status=400)
        
        return Response({'data': serializer.errors,'message': 'اطلاعات ورودی نامعتبر می باشد'}, status=400)
    
#---------------     

class VerifyCodeView(APIView):
    def post(self, request):
        data = request.data
        serializer = VerifyCodeSerializer(data=data)
        if serializer.is_valid():
            code = serializer.validated_data['verification_code']
            
            try:
                profile = Profile.objects.get(verification_code=code)
                
                # تولید توکن JWT
                token = RefreshToken.for_user(profile.user)
                
                # پاک کردن کد بعد از استفاده موفق
                profile.verification_code = None
                profile.save()
                
                return Response({
                    'message': 'ورود موفق',
                    'refresh': str(token),
                    'access': str(token.access_token)
                }, status=200)
            
            except Profile.DoesNotExist:
                return Response({'message': 'کد تایید نامعتبر است'}, status=400)
        
        return Response({'data': serializer.errors, 'message': 'اطلاعات ورودی نامعتبر می باشد'}, status=400)

#---------------  

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = serializer.validated_data["refresh"]
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "خروج موفق"}, status=205)
            except Exception:
                return Response({"message": "توکن نامعتبر"}, status=400)
        return Response({"data": serializer.errors, "message": "اطلاعات ورودی نامعتبر"}, status=400)

