from django.shortcuts import render
from django.views.generic.base import View

from apps.organizations.models import CourseOrg, City

class OrgView(View):
    def get(self, request, *args, **kwargs):
        all_orgs = CourseOrg.objects.all()
        org_nums = CourseOrg.objects.count()
        all_city = City.objects.all()
        return render(request, 'org-list.html', {
            'all_orgs' : all_orgs,
            'org_nums' : org_nums,
            'all_city' : all_city,
        })
