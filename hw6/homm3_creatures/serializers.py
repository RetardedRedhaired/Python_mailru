from rest_framework import serializers

from .models import Creature


class CreatureSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    level = serializers.IntegerField()
    descr = serializers.CharField()

    def create(self, validated_data):
        return Creature.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.descr = validated_data.get('descr', instance.descr)
        instance.level = validated_data.get('level', instance.level)
        instance.save()
        return instance
