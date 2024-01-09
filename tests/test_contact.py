import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from contact.models import Contact, ContactActivityLog, ContactGroup
from contact.serializers import ContactSerializer, ContactGroupSerializer


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

#!!!!ЗАДАНИЕ 5 - в исходной базе уже имеется решение, которое и скопировал сюда:)
# возможно есть смысл в дальнейшем удалить этот код с исходной базы
# или изменить задание подразумевающее как то дополнить тест на основе имеющегося
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


@pytest.mark.django_db
def test_contactgroup_create(contact_factory, mocker):
    contact1 = contact_factory(first_name="John", city="NY")
    contact2 = contact_factory(first_name="Jane", city="LA")
    contact_group = ContactGroup(name="group 1")
    contact_group.save()
    contact_group.contacts.add(contact1, contact2)
    contact_group.save()
    assert ContactGroup.objects.all().count() == 1
    try:
        contactgroup_db = ContactGroup.objects.get(pk=contact_group.pk)
        assert list(contactgroup_db.contacts.all()) == [contact1, contact2]
    except:
        assert False


@pytest.mark.django_db
def test_contactgroup_serializer(contact_factory, mocker):
    contact1 = contact_factory(first_name="John", city="NY")
    contact2 = contact_factory(first_name="Jane", city="LA")
    contact_group = ContactGroup(name="group 1")
    contact_group.save()
    contact_group.contacts.add(contact1, contact2)
    contact_group.save()
    serialized = ContactGroupSerializer(contact_group)
    assert serialized.data["name"] == "group 1"
    assert serialized.data["contacts"][0]['first_name'] == "John"
    assert serialized.data["contacts"][0]['city'] == "NY"
    assert serialized.data["contacts"][1]['first_name'] == "Jane"
    assert serialized.data["contacts"][1]['city'] == "LA"


@pytest.mark.django_db
def test_contact_mocked_delete(contact_factory, mocker):
    mock_delete = mocker.patch.object(Contact, 'delete', autospec=True)
    contact1 = contact_factory(first_name="John", city="NY")
    contact1.delete()
    mock_delete.assert_called()
    assert Contact.objects.all().count() == 1