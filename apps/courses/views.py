from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from pure_pagination import Paginator, PageNotAnInteger

from apps.courses.models import Course, CourseTag, CourseResource, Video
from apps.operation.models import UserFavorite, UserCourse, CourseComments

class VideoView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, video_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        video = Video.objects.get(id=int(video_id))

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')[:5]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course-play.html', {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "video": video,
        })

class CourseCommentsView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        comments = CourseComments.objects.filter(course=course)

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1
            course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')[:5]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course-comment.html', {
            "course" : course,
            "course_resources" : course_resources,
            "related_courses" : related_courses,
            "comments" : comments,
        })

class CourseLessonView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1
            course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')[:5]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course-video.html', {
            "course" : course,
            "course_resources" : course_resources,
            "related_courses" : related_courses,
        })

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

