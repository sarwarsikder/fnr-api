from rest_framework.permissions import BasePermission
from rest_framework.views import APIView

from adminapp.models import Comments
from rest_framework.pagination import PageNumberPagination
from serviceapp.serializers.comment_serializer import CommentSerializer

from adminapp.views.helper import LogHelper



class CommentPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method == 'GET':
                return True
            elif request.method == 'POST':
                return True
            return False
        return False


class CommentsViewSet(APIView):
    permission_classes = (CommentPermissions,)

    def get(self, request, **kwargs):
        task_id = kwargs['task_id']
        paginator = PageNumberPagination()
        paginator.page_size = 5
        comments = Comments.objects.filter(task_id=task_id).order_by('-created_at')
        result_page = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)
