from rest_framework.routers import DefaultRouter
from .views import BookViewSet, AuthorViewSet

app_name = "api"

router = DefaultRouter()
router.register(r"authors", viewset=AuthorViewSet, basename="authors")
router.register(r"books", viewset=BookViewSet, basename="books")

urlpatterns = router.urls
