from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from apps.organizations.models import CourseOrg, City
from apps.organizations.forms import AddAskForm

class AddAskView(View):
    def post(self, request, *args, **kwargs):
        userask_form = AddAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return JsonResponse({
                'status' : 'success'
            })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg' : '提交失败'
            })

class OrgView(View):
    def get(self, request, *args, **kwargs):
        all_orgs = CourseOrg.objects.all()
        all_citys = City.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        city_id = request.GET.get('city', '')
        if city_id:
            if city_id.isdigit():
                all_orgs = all_orgs.filter(city_id=int(city_id))

        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')

        org_nums = all_orgs.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, per_page=10, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs' : orgs,
            'org_nums' : org_nums,
            'all_citys' : all_citys,
            'category' : category,
            'city_id' : city_id,
            'sort' : sort,
            'hot_orgs' : hot_orgs,
        })
