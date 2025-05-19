from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from links.models import Link, LinkHit
from links.serializers import (
    LinkHitDetailedSerializer,
    LinkHitSerializer,
    LinkSerializer,
)


class LinkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows links to be viewed.
    """

    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    lookup_field = "link_hash"
    # permission_classes = [permissions.IsAuthenticated]

    @action(methods=["GET"], detail=True, serializer_class=LinkHitSerializer)
    def hits(self, request, link_hash: str):
        link = self.get_object()
        hits = link.link_hits.all()
        serializer = self.get_serializer(hits, many=True)
        return Response(serializer.data)


class LinkHitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows links to be viewed.
    """

    queryset = LinkHit.objects.select_related("link").all()
    serializer_class = LinkHitDetailedSerializer
    # permission_classes = [permissions.IsAuthenticated]


def redirect_view(request, link_hash: str) -> HttpResponse:
    link = get_object_or_404(Link, link_hash=link_hash)
    link.hits = F("hits") + 1
    link.save()

    LinkHit.objects.create(link=link)

    return HttpResponseRedirect(link.url)
