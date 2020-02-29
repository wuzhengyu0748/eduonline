from django.views.generic import View
from django.http import JsonResponse

from apps.operation.models import UserFavorite, CourseComments
from apps.operation.forms import UserFavoriteForm, CommentsForm
from apps.courses.models import Course
from apps.organizations.models import CourseOrg, Teacher

class CommentView(View):
    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({
                "status":"fail",
                "msg":"请先登录"
            })

        comment_form = CommentsForm(request.POST)
        if comment_form.is_valid():
            course = comment_form.cleaned_data['course']
            comments = comment_form.cleaned_data['comments']

            comment = CourseComments()
            comment.user = request.user
            comment.comments = comments
            comment.course = course
            comment.save()

            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })

class AddFavView(View):
    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({
                "status":"fail",
                "msg":"请先登录"
            })

        user_fav_form = UserFavoriteForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data['fav_id']
            fav_type = user_fav_form.cleaned_data['fav_type']

            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)

            if existed_records:
                existed_records.delete()
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_type == 2:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums -= 1
                    course_org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()

                return JsonResponse({
                    "status":"success",
                    "msg":"收藏"
                })
            else:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()

                return JsonResponse({
                    "status":"success",
                    "msg":"已收藏"
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })
