from django.conf import settings
from django.db import models


class Profile(models.Model):
    ROLE_CHOICES = [
        ("instructor", "مدرس"),
        ("student", "دانشجو"),
    ]

    # نام، ایمیل و رمز عبور در مدل آماده‌ی User قرار دارند.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="کاربر",
    )
    role = models.CharField("نقش", max_length=10, choices=ROLE_CHOICES, default="student")
    phone = models.CharField("شماره تماس", max_length=15, blank=True)
    bio = models.TextField("درباره من", blank=True)

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل‌ها"

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
