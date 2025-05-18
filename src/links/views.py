from rest_framework import permissions, viewsets, status
from links.models import Link
from links.serializers import LinkSerializer

from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.response import Response



class LinkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows links to be viewed.
    """
    queryset = Link.objects.all().order_by('-hits')
    serializer_class = LinkSerializer
    lookup_field = "link_hash"
    #permission_classes = [permissions.IsAuthenticated]


def redirect_view(request, link_hash: str) -> HttpResponse:
    link = get_object_or_404(Link, link_hash=link_hash)
    return HttpResponseRedirect(link.url)