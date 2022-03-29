from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Tags
from .serializers import TagsSerializer


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
