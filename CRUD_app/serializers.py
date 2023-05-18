from rest_framework import serializers
from .models import Box

class BoxSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Box
        fields = ['id', 'length', 'breadth', 'height', 'created_by', 'updated_at']
        read_only_fields = ['created_by']


    def create(self, validated_data):
        user = self.context['request'].user
        box = Box.objects.create(**validated_data)
        return box

class BoxListSerializer(serializers.ModelSerializer):

    created_by = serializers.ReadOnlyField(source='creator.username')
    area = serializers.SerializerMethodField()
    volume = serializers.SerializerMethodField()

    class Meta:
        model = Box
        fields = ['id', 'length', 'breadth','updated_at','created_at','created_by', 'height', 'volume', 'area']


    def get_area(self, object):
        return object.length * object.breadth

    def get_volume(self,object):
        return object.length * object.breadth * object.height

    def get_fields(self):
        fields = super().get_fields()

        user = self.context.get('request').user
        if user.is_staff:
            fields['created_by'] = serializers.CharField()
            fields['updated_at'] = serializers.CharField()
        else:
            del fields['created_by']
            del fields['updated_at']
            del fields['created_at']

        return fields














