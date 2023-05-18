from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import FloatField, F, Sum, Q
from django.db.models.functions import Cast
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework.exceptions import PermissionDenied

from .models import Box


class BoxService:

    @classmethod
    def __validate_create_request(cls, length, breadth, height):
        if length < 0 or breadth < 0 or height < 0:
            raise APIException("Invalid Dimensions")
        else:
            pass

    @classmethod
    def __check_average_area(cls, length, breadth):
        sum_of_areas = Box.objects.aggregate(sum_of_areas=Sum(F('length') * F('breadth')))['sum_of_areas']
        if sum_of_areas is None:
            sum_of_areas = 0
        current_area = length * breadth
        average_area = (sum_of_areas + current_area) / (Box.objects.count() + 1)

        if average_area is not None and average_area > settings.A1:
            print("something", average_area, settings.A1)
            raise APIException("Average area exceeded.")

    @classmethod
    def __check_average_volume(cls, length, breadth, height, user):
        box_created_by_user = Box.objects.filter(created_by=user)
        sum_of_volume = box_created_by_user.aggregate(
            sum_of_vol=Sum(F('length') * F('breadth') * F('height')))['sum_of_vol']
        if sum_of_volume is None:
            sum_of_volume = 0
        current_volume = length * breadth * height
        average_volume = (sum_of_volume + current_volume) / (box_created_by_user.count() + 1)

        if average_volume is not None and average_volume > settings.V1:
            raise APIException("Average volume exceeded for the current user.")

    @classmethod
    def __check_total_boxes_added_in_week(cls):
        week_start = timezone.now().date() - timedelta(days=7)
        week_box_count = Box.objects.filter(created_at__gte=week_start).count()

        if week_box_count >= settings.L1:
            raise APIException("Total boxes added in a week exceeded.")

    @classmethod
    def __check_total_boxes_added_in_week_for_user(cls, user):
        week_start = timezone.now().date() - timedelta(days=7)
        week_user_box_count = Box.objects.filter(created_by=user, created_at__gte=week_start).count()

        if week_user_box_count >= settings.L2:
            raise APIException("Total boxes added in a week exceeded for the current user.")

    @classmethod
    def filter_boxes(cls, queryset, params):
        length_more_than = params.get('length_more_than')
        length_less_than = params.get('length_less_than')
        breadth_more_than = params.get('breadth_more_than')
        breadth_less_than = params.get('breadth_less_than')
        height_more_than = params.get('height_more_than')
        height_less_than = params.get('height_less_than')
        area_more_than = params.get('area_more_than')
        area_less_than = params.get('area_less_than')
        volume_more_than = params.get('volume_more_than')
        volume_less_than = params.get('volume_less_than')

        if length_more_than:
            queryset = queryset.filter(length__gt=length_more_than)
        if length_less_than:
            queryset = queryset.filter(length__lt=length_less_than)
        if breadth_more_than:
            queryset = queryset.filter(breadth__gt=breadth_more_than)
        if breadth_less_than:
            queryset = queryset.filter(breadth__lt=breadth_less_than)
        if height_more_than:
            queryset = queryset.filter(height__gt=height_more_than)
        if height_less_than:
            queryset = queryset.filter(height__lt=height_less_than)
        if area_more_than:
            queryset = queryset.filter(Q(length__gt=area_more_than/F('breadth')) | Q(breadth__gt=area_more_than/F('length')))
        if area_less_than:
            queryset = queryset.filter(Q(length__lt=area_less_than/F('breadth')) | Q(breadth__lt=area_less_than/F('length')))
        if volume_more_than:
            queryset = queryset.filter(Q(length__gt=volume_more_than / (F('breadth') * F('height'))) | Q(breadth__gt=volume_more_than / (F('length') * F('height'))) | Q(height__gt=volume_more_than / (F('length') * F('breadth'))))
        if volume_less_than:
            queryset = queryset.filter(Q(length__lt=volume_less_than / (F('breadth') * F('height'))) | Q(breadth__lt=volume_less_than / (F('length') * F('height'))) | Q(height__lt=volume_less_than / (F('length') * F('breadth'))))
        return queryset

    @classmethod
    def staff_member_filter(cls, queryset, params):
        filter_user = params.get('user')
        if filter_user:
            queryset = queryset.filter(created_by__username=filter_user)
            # Filter by date created before a specific date
        date_filter_before = params.get('date_filter_before')
        if date_filter_before:
            try:
                date_filter_before = datetime.strptime(date_filter_before, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__lt=date_filter_before)
            except ValueError:
                pass

        # Filter by date created after a specific date
        date_filter_after = params.get('date_filter_after')
        if date_filter_after:
            try:
                date_filter_after = datetime.strptime(date_filter_after, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__gt=date_filter_after)
            except ValueError:
                pass
        return queryset

    @classmethod
    def create_box(cls, request):
        length = request.data.get("length")
        breadth = request.data.get("breadth")
        height = request.data.get("height")
        user = request.user

        cls.__validate_create_request(length, breadth, height)
        cls.__check_average_area(length, breadth)
        cls.__check_average_volume(length, breadth, height, user)
        cls.__check_total_boxes_added_in_week()
        cls.__check_total_boxes_added_in_week_for_user(user)

        Box.objects.create(length=length, breadth=breadth, height=height, created_by=user)

    @classmethod
    def delete_box(cls, request, *args, **kwargs):
        box_id = kwargs.get('pk')
        box = Box.objects.get(id=box_id)
        # Check if the user is the creator of the instance
        if box.created_by != request.user:
            raise PermissionDenied("You do not have permission to delete this object.")
        Box.objects.filter(id=box_id).delete()

    @classmethod
    def update_box(cls, request, *args, **kwargs):
        box_id = kwargs.get('pk')
        box = Box.objects.get(id=box_id)
        if request.user.is_staff:
            if request.data.get('length'):
                box.length = request.data.get('length')
            if request.data.get('breadth'):
                box.breadth = request.data.get('breadth')
            if request.data.get('height'):
                box.height = request.data.get('height')

            length = box.length
            breadth = box.breadth
            height = box.height
            user = request.user

            cls.__validate_create_request(length, breadth, height)
            cls.__check_average_area(length, breadth)
            cls.__check_average_volume(length, breadth, height, user)

            box.save()

        else:
            # If the user is not a staff user, return a 403 Forbidden response
            raise APIException('You are not authorized to perform this action.')
