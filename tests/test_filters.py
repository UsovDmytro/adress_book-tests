import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from contact.models import Contact
from contact.serializers import ContactSerializer


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def contact_factory():
    def factory(first_name, city):
        return Contact.objects.create(first_name=first_name, city=city)
    return factory

@pytest.mark.django_db
def test_filter_by_first_name(api_client, contact_factory):
    contact_factory(first_name="John", city="NY")
    contact_factory(first_name="Jane", city="LA")
    url = reverse('contact-list')

    response = api_client.get(url, {'first_name': 'John'})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['first_name'] == "John"

@pytest.mark.django_db
def test_filter_by_city(api_client, contact_factory):
    contact_factory(first_name="John", city="NY")
    contact_factory(first_name="Jane", city="LA")
    url = reverse('contact-list')

    response = api_client.get(url, {'city': 'NY'})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['city'] == "NY"


@pytest.fixture
def contact():
    return Contact.objects.create(
        first_name="John",
        last_name="Doe",
        country="USA",
        city="NY",
        street="Main street",
        url="https://example.com",
        phone="+1234567890",
        image=None  # можна додати зображення, якщо потрібно
    )


# Тест на перевірку серіалізації
@pytest.mark.django_db
def test_contact_serializer(contact):
    serialized = ContactSerializer(contact)

    assert serialized.data["first_name"] == "John"
    assert serialized.data["last_name"] == "Doe"
    assert serialized.data["country"] == "USA"
    assert serialized.data["city"] == "NY"
    assert serialized.data["street"] == "Main street"
    assert serialized.data["url"] == "https://example.com"
    assert serialized.data["phone"] == "+1234567890"
    assert serialized.data["image"] is None  # якщо у вас є зображення, перевірте його URL тут