from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import UserSerializer

@api_view(['GET'])
def me(request):
    if not request.user.is_authenticated():
        return HttpResponse(status=404)

    serializer = UserSerializer(request.user)
    return Response(serializer.data)
