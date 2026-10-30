from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from accounts.models import Profile


class Category(models.Model):
    name = models.CharField("موضوع", max_length=100, unique=True)
    description = models.TextField("توضیحات", blank=True)

    class Meta:
        verbose_name = "موضوع"
        verbose_name_plural = "موضوع‌ها"

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField("عنوان", max_length=200)
    description = models.TextField("توضیحات")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="courses",
        verbose_name="موضوع",
    )
    instructor = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name="teaching_courses",
        limit_choices_to={"role": "instructor"},
        verbose_name="مدرس",
    )
    capacity = models.PositiveIntegerField("ظرفیت", validators=[MinValueValidator(1)])
    start_time = models.DateTimeField("زمان شروع")
    end_time = models.DateTimeField("زمان پایان")
    price = models.DecimalField(
        "هزینه (تومان)",
        max_digits=12,
        decimal_places=0,
        default=0,
        validators=[MinValueValidator(0)],
    )
    created_at = models.DateTimeField("زمان ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "دوره"
        verbose_name_plural = "دوره‌ها"

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError({"end_time": "پایان دوره باید بعد از شروع آن باشد."})


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="دوره",
    )
    title = models.CharField("عنوان جلسه", max_length=200)
    number = models.PositiveIntegerField("شماره جلسه", validators=[MinValueValidator(1)])
    description = models.TextField("توضیحات", blank=True)
    start_time = models.DateTimeField("زمان شروع")
    end_time = models.DateTimeField("زمان پایان")

    class Meta:
        verbose_name = "جلسه"
        verbose_name_plural = "جلسه‌ها"
        ordering = ["course", "number"]
        unique_together = [("course", "number")]

    def __str__(self):
        return f"{self.course.title} - جلسه {self.number}: {self.title}"

    def clean(self):
        super().clean()
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError({"end_time": "پایان جلسه باید بعد از شروع آن باشد."})
