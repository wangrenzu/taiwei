from rest_framework import serializers

from .models import Design, Tags, Size, Script, Collocation


class DesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Design
        fields = "__all__"


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"


class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = "__all__"


class CollocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collocation
        fields = "__all__"
