from django.contrib import admin

from .models import Project, SiteProfile


class OwnerOnlyAdminSite(admin.AdminSite):
    site_header = "WESTY — панель власника"
    site_title = "WESTY"
    index_title = "Керування сайтом"

    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser


owner_admin_site = OwnerOnlyAdminSite(name="admin")


@admin.register(Project, site=owner_admin_site)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "year", "featured", "is_published", "sort_order")
    list_filter = ("is_published", "featured", "category", "year")
    list_editable = ("featured", "is_published", "sort_order")
    search_fields = ("title", "summary", "description", "technologies")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-featured", "sort_order", "-created_at")
    fieldsets = (
        ("Основне", {"fields": ("title", "slug", "summary", "description", "category")}),
        ("Вигляд і технології", {"fields": ("image_url", "technologies", "year")}),
        ("Посилання", {"fields": ("project_url", "source_url")}),
        ("Публікація", {"fields": ("featured", "is_published", "sort_order")}),
    )


@admin.register(SiteProfile, site=owner_admin_site)
class SiteProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Профіль", {"fields": ("name", "role", "headline", "bio", "years_experience")}),
        ("Зв'язок", {"fields": ("telegram_username", "phone", "email", "availability")}),
    )

    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

