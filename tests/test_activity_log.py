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
def test_activity_log_create(contact_factory):
    contact1 = contact_factory(first_name="John", city="NY")
    contact2 = contact_factory(first_name="Jane", city="LA")
    try:
       act_log = ContactActivityLog.objects.get(contact=contact1)
       assert act_log.contact == contact1
    except:
        assert False

@pytest.mark.django_db
def test_activity_log_edit(contact_factory):
    contact1 = contact_factory(first_name="John", city="NY")
    contact2 = contact_factory(first_name="Jane", city="LA")
    contact1.first_name = 'Doe'
    contact1.save()
    try:
       act_log = ContactActivityLog.objects.get(contact=contact1, activity_type="EDITED")
       assert act_log.contact == contact1
    except:
        assert False


@pytest.mark.django_db
def test_activity_log_mocked_create(contact_factory, mocker):
    mock_create = mocker.patch.object(ContactActivityLog, 'save', autospec=True)
    contact1 = contact_factory(first_name="John", city="NY")
    contact2 = contact_factory(first_name="Jane", city="LA")
    contact1.first_name = 'Doe'
    contact1.save()
    assert mock_create.call_count == 3
    assert mock_create.call_args[0][0].activity_type == "EDITED"
    try:
       contact_db = Contact.objects.get(pk=contact1.pk)
       assert contact_db.first_name == 'Doe'
    except:
        assert False
