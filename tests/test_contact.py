import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from contact.models import Contact, ContactActivityLog
from contact.serializers import ContactSerializer


@pytest.fixture
def contact_factory():
    def factory(first_name, city):
        return Contact.objects.create(first_name=first_name, city=city)
    return factory


@pytest.mark.django_db
def test_contact_mocked_create(contact_factory, mocker):
    mock_create = mocker.patch.object(Contact, 'save', autospec=True)
    contact1 = contact_factory(first_name="John", city="NY")
    contact2 = contact_factory(first_name="Jane", city="LA")
    assert Contact.objects.all().count() == 0

