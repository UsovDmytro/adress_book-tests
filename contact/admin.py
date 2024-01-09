# admin.py
from django.contrib import admin
from contact.models import Contact, ContactGroup, ContactActivityLog

admin.site.register(Contact)
admin.site.register(ContactGroup)
admin.site.register(ContactActivityLog)
