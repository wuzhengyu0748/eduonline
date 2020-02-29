from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, PageNotAnInteger

from apps.courses.models import Course, CourseTag
from apps.operation.models import UserFavorite

class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course =True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tags = course.coursetag_set.all()
        tag_list = [tag.tag for tag in tags]

        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course_id=course.id)
        related_course = set()
        for course_tag in course_tags:
            related_course.add(course_tag.course)

        return render(request, 'course-detail.html', {
            "course" : course,
            "has_fav_course" : has_fav_course,
            "has_fav_org" : has_fav_org,
            "related_course" : related_course,
        })

class CourseListView(View):
    def get(self, request, *args, **kwargs):
        all_courses = Course.objects.order_by("-add_time")
        hot_courses = Course.objects.order_by('-click_nums')[:3]

        sort = request.GET.get("sort", "")
        if sort == 'students':
            all_courses = all_courses.order_by('-students')
        elif sort == 'hot':
            all_courses = all_courses.order_by('-click_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, per_page=10, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html',{
            'all_courses' : courses,
            'sort' : sort,
            'hot_courses' : hot_courses,
        })

