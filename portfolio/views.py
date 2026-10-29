from django.shortcuts import render

from .models import Project, SiteProfile


def home(request):
    profile = SiteProfile.get_profile()
    projects = list(Project.objects.filter(is_published=True))
    categories = sorted({project.category for project in projects if project.category})
    context = {
        "profile": profile,
        "projects": projects,
        "categories": categories,
        "project_count": len(projects),
    }
    return render(request, "portfolio/home.html", context)
