from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class SiteProfile(models.Model):
    name = models.CharField("Ім'я або бренд", max_length=80, default="WESTY")
    role = models.CharField(
        "Спеціалізація", max_length=120, default="Розробник цифрових продуктів"
    )
    headline = models.CharField(
        "Заголовок на головному екрані",
        max_length=180,
        default="Створюю цифрові речі, які хочеться відкривати.",
    )
    bio = models.TextField(
        "Про мене",
        blank=True,
        default=(
            "Поєдную дизайн, технології та увагу до деталей, щоб перетворювати "
            "ідеї на швидкі, зрозумілі й незабутні цифрові продукти."
        ),
    )
    years_experience = models.PositiveSmallIntegerField(
        "Років досвіду",
        default=2,
        validators=[MinValueValidator(0), MaxValueValidator(99)],
    )
    telegram_username = models.CharField(
        "Telegram username", max_length=40, default="managerwesty"
    )
    phone = models.CharField("Телефон", max_length=32, default="+380693904928")
    email = models.EmailField("Електронна пошта", blank=True)
    availability = models.CharField(
        "Статус доступності", max_length=80, default="Відкритий до цікавих проєктів"
    )
    updated_at = models.DateTimeField("Оновлено", auto_now=True)

    class Meta:
        verbose_name = "Профіль"
        verbose_name_plural = "Профіль"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_profile(cls):
        profile, _ = cls.objects.get_or_create(pk=1)
        return profile


class Project(models.Model):
    title = models.CharField("Назва проєкту", max_length=120)
    slug = models.SlugField("Посилання", max_length=140, unique=True, blank=True)
    summary = models.CharField("Короткий опис", max_length=220)
    description = models.TextField("Детальний опис", blank=True)
    category = models.CharField("Категорія", max_length=60, default="Веброзробка")
    technologies = models.CharField(
        "Технології через кому", max_length=240, blank=True
    )
    image_url = models.URLField("Посилання на обкладинку", blank=True)
    project_url = models.URLField("Посилання на проєкт", blank=True)
    source_url = models.URLField("Посилання на код", blank=True)
    year = models.PositiveSmallIntegerField("Рік", blank=True, null=True)
    featured = models.BooleanField("Вибраний проєкт", default=False)
    is_published = models.BooleanField("Опублікований", default=True)
    sort_order = models.PositiveSmallIntegerField("Порядок показу", default=0)
    created_at = models.DateTimeField("Створено", auto_now_add=True)
    updated_at = models.DateTimeField("Оновлено", auto_now=True)

    class Meta:
        ordering = ("-featured", "sort_order", "-created_at")
        verbose_name = "Проєкт"
        verbose_name_plural = "Проєкти"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "project"
            slug = base_slug
            counter = 2
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def technology_list(self):
        return [item.strip() for item in self.technologies.split(",") if item.strip()]
