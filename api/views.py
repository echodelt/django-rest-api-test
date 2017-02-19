from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer
from .permissions import ApiAccessPermission

class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows articles to be viewed or edited.
    """
    queryset = Article.objects.all().order_by('-publication_date')
    serializer_class = ArticleSerializer
