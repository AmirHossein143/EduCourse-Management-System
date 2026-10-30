from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from accounts.models import Profile
from courses.models import Course


class Enrollment(models.Model):
    student = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name="enrollments",
        limit_choices_to={"role": "student"},
        verbose_name="دانشجو",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="دوره",
    )
    enrolled_at = models.DateTimeField("زمان ثبت‌نام", auto_now_add=True)
    # تا زمانی که مدرس نمره‌ای ثبت نکرده، مقدار این فیلد خالی است.
    grade = models.DecimalField(
        "نمره",
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
    )
    evaluation = models.TextField("ارزیابی مدرس", blank=True)

    class Meta:
        verbose_name = "ثبت‌نام"
        verbose_name_plural = "ثبت‌نام‌ها"
        unique_together = [("student", "course")]

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title}"
