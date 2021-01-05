from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render, resolve_url
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import AnonymousUser

from .serializers import CreatureSerializer
from .models import Creature
from .forms import NameForm
from .tasks import mail_to_admin
from urllib.parse import urlparse


def login(request):
    return render(request, 'login.html')


@login_required
def home(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect('')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'home.html', {'form': form})


def is_authorized(method_to_decorate, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    def wrapper(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            return redirect_to_login(path, resolved_login_url, redirect_field_name)
        return method_to_decorate(self, request, *args, **kwargs)
    return wrapper


class CreatureView(APIView):
    def get(self, request):
        creatures = Creature.objects.all()
        serializer = CreatureSerializer(creatures, many=True)
        return Response({'creatures': serializer.data})

    @is_authorized
    def post(self, request):
        usr = request.user
        creatures = request.data.get('creatures')
        serializer = CreatureSerializer(data=creatures, many=True)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            print('TEST0')
            mail_to_admin.delay(usr.email)
            print('TEST')
            return Response({"success": "Creature '{}' created successfully".format(creatures[0].get('name'))})
        else:
            raise Http404("Something wrong")

    @is_authorized
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

    @is_authorized
    def delete(self, request, pk):
        try:
            creature = Creature.objects.all()
            saved_creature = creature.get(pk=pk)
        except Creature.DoesNotExist:
            return Response({"There is no such id"}, status=404)
        saved_creature.delete()
        return Response({
            "message": "Creature with id `{}` has been deleted.".format(pk)
        }, status=204)
