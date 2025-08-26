from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    """
    احراز هویت با ایمیل به جای یوزرنیم
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # جستجو کاربر با ایمیل
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        # چک کردن پسورد
        if user.check_password(password):
            return user
        return None
