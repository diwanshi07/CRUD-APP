from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Box
from .serializers import BoxListSerializer, BoxSerializer
from .services import BoxService


class BoxDeleteViewSet(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):

        try:
            BoxService.delete_box(request, *args, **kwargs)
            return Response(data="Deleted Successfully.", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BoxCreateViewSet(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        try:
            BoxService.create_box(request)
            return Response(data="Created Successfully.", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BoxListViewSet(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        try:
            queryset = Box.objects.all()

            # If the user wants to view the list of boxes created by them
            created_by_me = request.GET.get('my_boxes', None)
            if request.user.is_authenticated and created_by_me and created_by_me.lower() == 'true':
                queryset = queryset.filter(created_by=request.user)

            # If the user is a staff member
            elif request.user.is_authenticated and request.user.is_staff:
                queryset = BoxService.staff_member_filter(queryset, request.query_params)

            queryset = BoxService.filter_boxes(queryset, request.query_params)

            serializer = BoxListSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class BoxUpdateViewSet(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, *args, **kwargs):
        try:
            BoxService.update_box(request, *args, **kwargs)
            return Response(data="Updated Successfully.", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
