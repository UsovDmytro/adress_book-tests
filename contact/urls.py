from django.urls import path, include
from rest_framework.routers import DefaultRouter

from contact.views import ContactViewSet, ContactGroupViewSet

router = DefaultRouter()
router.register(r'contact-groups', ContactGroupViewSet)
router.register(r'', ContactViewSet)


urlpatterns = [
    path('', include(router.urls)),

]
