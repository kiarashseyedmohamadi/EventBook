from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Venue,User,Event,Booking

#-----------    

class VenueViewTest(TestCase):
   def setUp(self):
      self.client = APIClient()
      self.admin_user = User.objects.create_superuser(username="admin",email="admin@example.com",password="admin123")
      self.client.force_authenticate(user=self.admin_user)
      
      for i in range (10):
         Venue.objects.create(venue_title=f"سالن {i}",address=f"تهران {i}",description=f"توضیحات {i}",slug=f"s{i}")
      
      for i in range(5):
        Venue.objects.create(venue_title="سالن شیرودی",address=f"تهران منطقه {i}",description=f"توضیحات شیرودی {i}",slug=f"shiroodi{i}")
        
#-----------    

   def test_venue_list(self):
        url = reverse('events:venue-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
#-----------    
        
   def test_venue_filter_by_venue_title (self):
      url = reverse('events:venue-list') + '?venue_title=سالن شیرودی'
      response=self.client.get(url)
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.data['results'][0]['venue_title'], 'سالن شیرودی')
      for venue in response.data['results']:
         self.assertEqual(venue['venue_title'], 'سالن شیرودی')
       
#-----------    
      
   def test_venue_filter_by_address(self):
      url = reverse('events:venue-list') + '?address=تهران منطقه 0'
      response = self.client.get(url)
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.data['results'][0]['address'], 'تهران منطقه 0')
      for venue in response.data['results']:
            self.assertEqual(venue['address'], 'تهران منطقه 0')
            
#-----------    
 
   def test_get_venue(self):
        url = reverse('events:venue-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data['results']), 0)

#-----------    
        
   def test_post_venue(self):
      url = reverse('events:venue-list')
      data = {"venue_title": "سالن تست","address": "تهران، تست","description": "توضیحات تست","slug": "test-venue"}
      response = self.client.post(url, data, format="json")
      self.assertEqual(response.status_code, 201)
 
#-----------           
      
   def test_put_venue(self):
      venue= Venue.objects.first()
      url = reverse('events:venue-detail',args=[venue.id])
      data = {"venue_title": "سالن آپدیت","address": venue.address,"description": venue.description,"slug": venue.slug}
      response = self.client.put(url, data, format="json")
      self.assertEqual(response.status_code, 200) 
      venue.refresh_from_db()
      self.assertEqual(venue.venue_title, "سالن آپدیت")
   
#-----------   
   
   def test_patch_venue(self):
      venue= Venue.objects.first()
      url = reverse('events:venue-detail',args=[venue.id])
      data = {"venue_title": "سالن دومین آپدیت"}
      response = self.client.patch(url, data, format="json")
      self.assertEqual(response.status_code, 200)
      venue.refresh_from_db()
      self.assertEqual(venue.venue_title, "سالن دومین آپدیت")

#-----------   

   def test_delete_venue(self):
      venue= Venue.objects.first()
      self.assertIsNotNone(venue) 
      url = reverse('events:venue-detail',args=[venue.id])
      response = self.client.delete(url)
      self.assertEqual(response.status_code, 200)
      self.assertFalse(Venue.objects.filter(id=venue.id).exists())
  
#-----------    
      
   def test_venue_pagination(self):
      url = reverse('events:venue-list')  
      response = self.client.get(url)
      self.assertEqual(response.status_code, 200)
      self.assertEqual(len(response.data['results']), 10)
      self.assertEqual(response.data['count'], 15)
      response_page2=self.client.get(url + '?page=2')
      self.assertEqual(response_page2.status_code, 200)
      self.assertEqual(len(response_page2.data['results']), 5)
      
#========================================================================================================

class EventViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123"
        )
        self.client.force_authenticate(user=self.admin_user)

        # یک سالن برای همه‌ی رویدادها
        self.venue = Venue.objects.create(
            venue_title="سالن اصلی",
            address="تهران",
            description="توضیحات سالن اصلی",
            slug="main-venue"
        )

        # ایجاد ۱۵ رویداد با slug یکتا => pagination صفحه‌ی دوم هم وجود دارد
        for i in range(15):
            Event.objects.create(
                title=f"رویداد {i}",
                venue=self.venue,
                seats_total=100,
                seats_left=50,
                price=50000,
                organizer=self.admin_user,
                slug=f"roidad-{i}"
            )

    # ---------------------------
    def test_event_list(self):
        url = reverse('events:event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data['results']), 1)

    # ---------------------------
    def test_post_event(self):
        url = reverse('events:event-list')
        data = {
            "title": "رویداد تست",
            "venue": self.venue.id,
            "seats_total": 100,
            "seats_left": 100,
            "price": 70000,
            "slug": "roidad-test-event",
            "organizer": self.admin_user.id
        }
        response = self.client.post(url, data, format="json")
        # بعضی ویوها 200 برمی‌گردونن، بعضی‌ها 201 — هر دو قبول است
        self.assertIn(response.status_code, (200, 201))
        self.assertTrue(Event.objects.filter(title="رویداد تست").exists())

    # ---------------------------
    def test_put_event(self):
        event = Event.objects.first()
        url = reverse('events:event-detail', args=[event.id])
        data = {
            "title": "رویداد آپدیت",
            "venue": event.venue.id,
            "seats_total": event.seats_total,
            "seats_left": event.seats_left,
            "price": 80000,
            "slug": f"{event.slug}-updated",   # یکتا نگه می‌دارد
            "organizer": event.organizer.id
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        event.refresh_from_db()
        self.assertEqual(event.title, "رویداد آپدیت")
        self.assertEqual(event.price, 80000)

    # ---------------------------
    def test_patch_event(self):
        event = Event.objects.first()
        url = reverse('events:event-detail', args=[event.id])
        data = {"title": "رویداد دومین آپدیت"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        event.refresh_from_db()
        self.assertEqual(event.title, "رویداد دومین آپدیت")

    # ---------------------------
    def test_delete_event(self):
        event = Event.objects.first()
        url = reverse('events:event-detail', args=[event.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Event.objects.filter(id=event.id).exists())

    # ---------------------------
    def test_event_pagination(self):
        url = reverse('events:event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 10)

        response_page2 = self.client.get(url + '?page=2')
        self.assertEqual(response_page2.status_code, 200)

#========================================================================================================

class BookingViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # کاربر عادی
        self.user = User.objects.create_user(email='arezoo@yahoo.com', password='123456')
        self.client.force_authenticate(user=self.user)

        # یک سالن و یک رویداد
        self.venue = Venue.objects.create(
            venue_title="سالن تست",
            address="تهران",
            description="توضیحات سالن",
            slug="test-venue"
        )

        self.event = Event.objects.create(
            title="رویداد تست",
            venue=self.venue,
            seats_total=100,
            seats_left=100,
            price=50000,
            slug="test-event",
            organizer=self.user
        )

        # یک رزرو اولیه
        self.booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            ticket_count=2
        )

    # ---------------------------
    def test_get_bookings(self):
        url = reverse('events:booking-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['ticket_count'], 2)

    # ---------------------------
    def test_create_booking_success(self):
        url = reverse('events:booking-list')
        data = {"event": self.event.id, "ticket_count": 3}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

        # ظرفیت صندلی کاهش پیدا کرده باشه
        self.event.refresh_from_db()
        self.assertEqual(self.event.seats_left, 95)

        # رزرو ایجاد شده
        self.assertTrue(Booking.objects.filter(user=self.user, ticket_count=3).exists())

    # ---------------------------
    def test_create_booking_insufficient_seats(self):
        url = reverse('events:booking-list')
        data = {"event": self.event.id, "ticket_count": 200}  # بیش از ظرفیت
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("ظرفیت کافی وجود ندارد", response.data['message'])

    # ---------------------------
    def test_create_booking_invalid_ticket_count(self):
        url = reverse('events:booking-list')
        data = {"event": self.event.id, "ticket_count": 0}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("تعداد رزرو باید بزرگتر از صفر باشد", response.data['message'])

    # ---------------------------
    def test_delete_booking_success(self):
        url = reverse('events:booking-detail', args=[self.booking.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())

        # صندلی‌ها برگرده
        self.event.refresh_from_db()
        self.assertEqual(self.event.seats_left, 100)

    # ---------------------------
    def test_delete_booking_forbidden(self):
        # کاربر دیگه‌ای بساز
        other_user = User.objects.create_user(email="other@example.com", password="123456")
        self.client.force_authenticate(user=other_user)

        url = reverse('events:booking-detail', args=[self.booking.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Booking.objects.filter(id=self.booking.id).exists())
        
#=======================================================================================================      

class PaymentViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='arezoo@yahoo.com', password='123456')
        self.client.force_authenticate(user=self.user)

        # سالن و رویداد
        self.venue = Venue.objects.create(
            venue_title="سالن تست",
            address="تهران",
            description="توضیحات سالن",
            slug="test-venue"
        )

        self.event = Event.objects.create(
            title="رویداد تست",
            venue=self.venue,
            seats_total=100,
            seats_left=100,
            price=50000,
            slug="test-event",
            organizer=self.user
        )

        self.booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            ticket_count=2
        )

    def test_get_payment_not_exist(self):
        url = reverse('events:payment-detail', args=[self.booking.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertIn('پرداختی برای این رزرو وجود ندارد', response.data['message'])

    def test_post_payment_success(self):
        url = reverse('events:payment-list', args=[self.booking.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)
        self.assertIn('payment', response.data)
        self.booking.refresh_from_db()
        self.assertTrue(hasattr(self.booking, 'payment'))
        self.assertEqual(self.booking.payment.status, 'success')

    def test_post_payment_already_paid(self):
        self.booking.payment = Payment.objects.create(booking=self.booking, amount=50000, ref='test123', status='success')
        self.booking.save()
        url = reverse('events:payment-list', args=[self.booking.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
        self.assertIn('پرداخت قبلاً انجام شده', response.data['message'])

    def test_post_payment_forbidden(self):
        other_user = User.objects.create_user(email="other@example.com", password="123456")
        self.client.force_authenticate(user=other_user)
        url = reverse('events:payment-list', args=[self.booking.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertIn('شما اجازه پرداخت این رزرو را ندارید', response.data['message'])

#=======================================================================================================

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin123')
        self.client.force_authenticate(user=self.staff_user)

    def test_register_post(self):
        url = reverse('events:register-list')
        data = {"username": "user1", "email": "user1@example.com", "password": "123456"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="user1").exists())

    def test_register_get_staff(self):
        url = reverse('events:register-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_register_get_non_staff_forbidden(self):
        user = User.objects.create_user(username="normal", email="normal@example.com", password="123456")
        self.client.force_authenticate(user=user)
        url = reverse('events:register-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_register_put_patch_delete(self):
        # ایجاد کاربر
        user = User.objects.create_user(username="testuser", email="t@example.com", password="123456")

        # PUT
        url = reverse('events:register-detail', args=[user.id])
        data = {"username": "updated", "email": "upd@example.com", "password": "123456"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        user.refresh_from_db()
        self.assertEqual(user.username, "updated")

        # PATCH
        data_patch = {"username": "patched"}
        response = self.client.patch(url, data_patch, format="json")
        self.assertEqual(response.status_code, 201)
        user.refresh_from_db()
        self.assertEqual(user.username, "patched")

        # DELETE
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(id=user.id).exists())

#=======================================================================================================

class AuthViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="123456")
        Profile.objects.create(user=self.user)

    def test_login_success_sends_email(self):
        url = reverse('events:login')
        data = {"email": "testuser@example.com", "password": "123456"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['requires_verification'])
        self.assertEqual(len(mail.outbox), 1)  # ایمیل ارسال شده

    def test_verify_code_success(self):
        profile = Profile.objects.get(user=self.user)
        profile.verification_code = "12345"
        profile.save()
        url = reverse('events:verify-code')
        data = {"verification_code": "12345"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        profile.refresh_from_db()
        self.assertIsNone(profile.verification_code)

    def test_verify_code_invalid(self):
        url = reverse('events:verify-code')
        data = {"verification_code": "00000"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_logout_success(self):
        token = RefreshToken.for_user(self.user)
        url = reverse('events:logout')
        data = {"refresh": str(token)}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 205)

    def test_logout_invalid_token(self):
        url = reverse('events:logout')
        data = {"refresh": "invalidtoken"}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
