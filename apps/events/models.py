from django.db import models
from django.contrib.auth.models import User

#--------------------------------------

def upload_image_venue(instance,filename):
    return f'images/venue{filename}'

class Venue(models.Model):
    venue_title = models.CharField(max_length = 255,verbose_name='عنوان محل برگزاری')
    address = models.TextField(verbose_name='آدرس محل برگزاری')
    description = models.TextField(verbose_name='توضیحات')
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to = upload_image_venue,verbose_name=' تصویر رویداد',null=True,blank=True)
        
    def __str__(self):
        return self.venue_title


    class Meta:
        verbose_name= 'محل برگزاری'
        verbose_name_plural= 'محل های محل برگزاری ها'
        
#--------------------------------------

def upload_image_event(instance,filename):
    return f'images/event{filename}'

class Event(models.Model):
    STATUS_CHOICES = [('ongoing', 'ongoing'), ('held', 'held'), ('cancelled', 'Cancelled'),('soldout','soldout')]
    
    title = models.CharField(max_length = 255)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="سازنده رویداد")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    venue = models.ForeignKey(Venue,on_delete=models.CASCADE,verbose_name=' محل برگزاری')
    seats_total = models.PositiveIntegerField()
    seats_left = models.PositiveIntegerField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد ')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ")
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to = upload_image_event,verbose_name=' تصویر رویداد',null=True,blank=True)
        
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name= 'رویداد'
        verbose_name_plural= 'رویداد ها'
        
#--------------------------------------

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="رویداد")
    ticket_count = models.PositiveIntegerField("تعداد بلیط", default=1)
    
    class Meta:
        verbose_name= 'رزرو '
        verbose_name_plural= 'رزرو ها'
    
#--------------------------------------

class Payment(models.Model):
    STATUS_CHOICES = [("pending", "در انتظار"),("success", "موفق"),("failed", "ناموفق"),]
    
    booking = models.OneToOneField("Booking", on_delete=models.CASCADE, related_name="payment")
    ref = models.CharField(max_length=50, unique=True,null=True,blank=True, verbose_name="شماره پیگیری")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"پرداخت {self.ref} - {self.status}"
    
    class Meta:
        verbose_name= 'پرداخت'
        verbose_name_plural= 'پرداخت ها'
        
#-------------------------------------- 
    