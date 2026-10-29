from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Project, SiteProfile


class PortfolioPageTests(TestCase):
    def test_home_page_renders_editable_profile_defaults_and_contact(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "WESTY")
        self.assertContains(response, "managerwesty")
        self.assertContains(response, "+380693904928")
        self.assertContains(response, "Тут скоро будуть")

    def test_published_projects_appear_but_drafts_do_not(self):
        Project.objects.create(
            title="Сайт кав'ярні",
            summary="Лендінг для локальної кав'ярні",
            category="Веброзробка",
            technologies="Django, CSS",
            is_published=True,
        )
        Project.objects.create(
            title="Чернетка",
            summary="Ще не готово",
            is_published=False,
        )

        response = self.client.get(reverse("home"))

        self.assertContains(response, "Сайт кав&#x27;ярні")
        self.assertNotContains(response, "Чернетка")

    def test_admin_can_create_and_delete_projects(self):
        user = get_user_model().objects.create_superuser(
            username="portfolio-admin",
            email="admin@example.com",
            password="safe-test-password",
        )
        self.client.force_login(user)

        add_response = self.client.post(
            reverse("admin:portfolio_project_add"),
            {
                "title": "Portfolio demo",
                "summary": "A demo project",
                "description": "",
                "category": "Web",
                "technologies": "Django, CSS",
                "image_url": "",
                "project_url": "",
                "source_url": "",
                "year": "2026",
                "sort_order": "0",
                "is_published": "on",
                "_save": "Save",
            },
        )
        project = Project.objects.get(title="Portfolio demo")
        self.assertEqual(add_response.status_code, 302)

        delete_response = self.client.post(
            reverse("admin:portfolio_project_delete", args=[project.pk]),
            {"post": "yes"},
        )
        self.assertEqual(delete_response.status_code, 302)
        self.assertFalse(Project.objects.filter(pk=project.pk).exists())

    def test_staff_without_superuser_access_cannot_enter_admin(self):
        user = get_user_model().objects.create_user(
            username="staff-only",
            password="safe-test-password",
            is_staff=True,
            is_superuser=False,
        )
        self.client.force_login(user)

        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)
