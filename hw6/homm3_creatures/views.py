from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CreatureSerializer
from .models import Creature


class CreatureView(APIView):
    def get(self, request):
        creatures = Creature.objects.all()
        serializer = CreatureSerializer(creatures, many=True)
        return Response({'creatures': serializer.data})

    def post(self, request):
        creatures = request.data.get('creatures')
        serializer = CreatureSerializer(data=creatures, many=True)
        if serializer.is_valid(raise_exception=False):
            creature_saved = serializer.save()
            return Response({"success": "Creature '{}' created successfully".format(creatures[0].get('name'))})
        else:
            raise Http404("Something wrong")

    def put(self, request, pk):
        try:
            creature = Creature.objects.all()
            saved_creature = creature.get(pk=pk)
        except Creature.DoesNotExist:
            return Response({"There is no such id"}, status=404)
        data = request.data.get('creatures')
        serializer = CreatureSerializer(instance=saved_creature, data=data, partial=True)
        if serializer.is_valid(raise_exception=False):
            creature_saved = serializer.save()
            return Response({"success": "Creature '{}' updated successfully".format(creatures[0].get('name'))})
        else:
            return Response({"Serializer error"}, status=404)

    def delete(self, request, pk):
        try:
            creature = Creature.objects.all()
            saved_creature = creature.get(pk=pk)
        except Creature.DoesNotExist:
            return Response({"There is no such id"}, status=404)
        creature.delete()
        return Response({
            "message": "Creature with id `{}` has been deleted.".format(pk)
        }, status=204)