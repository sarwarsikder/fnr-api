import re, random, string, hashlib, json
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from rest_framework import viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from adminapp.models import Users, ResetPassword
from serviceapp.serializers.user_serializer import UserSerializer
from django.http import JsonResponse
from django.conf import settings
import io, os
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from adminapp.views.common_views import CommonView
from adminapp.views.helper import LogHelper


class UserProfilePermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False


class UserUploadPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.type == 'admin':
            return True
        elif request.user.is_authenticated and request.method in ['GET', 'PUT', 'PATCH', 'POST']:
            return True
        return False


class UserInfo(APIView):
    permission_classes = (UserProfilePermissions, )

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs ):
        try:
            partial = kwargs.pop('partial', True)
            instance = Users.objects.get(id=request.user.id)

            serializer = UserSerializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance, request.data)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                "message": "Something went wrong. please try again"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordRequestViewSet:

    @api_view(["post"])
    def forget_password(request):
        try:
            response = {}
            email = request.data.pop("email", '')
            users = Users.objects.filter(email=email, is_active=1)
            if users.exists():
                user = users[0]
                current_time = datetime.now()
                expired_date = current_time + timedelta(hours=1)
                reset_code = user.resetpassword_set.filter(already_used=0, expired_at__gt=current_time)
                if reset_code.exists():
                    hash_code = reset_code[0].hash_code
                    ResetPassword.objects.filter(id=reset_code[0].id).update(expired_at=expired_date)
                else:
                    # generate hash code and store
                    key = ''.join(
                        random.choice(string.ascii_letters + string.digits + string.ascii_letters) for _ in
                        range(10)) + str(datetime.now())
                    key = key.encode('utf-8')
                    hash_code = hashlib.sha224(key).hexdigest()
                    ResetPassword(user=user, hash_code=hash_code, expired_at=expired_date).save()
                base_url = settings.SITE_URL
                mail_template = "mails/reset_password.html"
                context = {
                    'base_url': base_url,
                    'key': hash_code
                }
                subject = "Supplementer ::Password Reset"
                to = user.email
                CommonView.sendEmail(request, mail_template, context, subject, to, user.id)
                response['success'] = True
                response['message'] = "A reset password email is sent to you with confirmation link"
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'message': "Email doesn't found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            LogHelper.efail(e)
            return Response({'success': False, 'message': "Something went wrong."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class UploadsView(APIView):
#
#     permission_classes = (UserUploadPermissions, )
#
#     def post(self, request, format=None):
#         response = {}
#         try:
#             avatar = request.FILES.get('avatar')
#             uploaded_image = io.BytesIO(avatar.read())
#             image = Image.open(uploaded_image)
#             old_image = image
#             output_image = io.BytesIO()
#             image.save(output_image, old_image.format)
#             custom_filename = "avatar_" + str(CommonView.getCurrentintTime(request)) + "." + image.format
#             file_path = "public/images/" + custom_filename
#             avatar_url = CommonView.uploadFileToS3(self, output_image, file_path, old_image)
#             if avatar_url['success']:
#                 Users.objects.filter(id=request.user.id).update(avatar=avatar_url['path'])
#                 response['avatar'] = avatar_url['path']
#                 response['message'] = "successfully updated profile image"
#             return Response(response, status=status.HTTP_200_OK)
#         except Exception as e:
#             print(e)
#             response = {
#                 "message": "Something went wrong. please try again"
#             }
#             return Response(response, status=status.HTTP_400_BAD_REQUEST)
