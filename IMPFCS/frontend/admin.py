from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from frontend.models import BasicInfo, AthleteInfo


class BasicInfoInline(admin.StackedInline):
    model = BasicInfo
    can_delete = False
    verbose_name_plural = 'basic information'


class AthleteInfoInline(admin.StackedInline):
    model = AthleteInfo
    can_delete = False
    verbose_name_plural = 'athlete information'


class THUUserAdmin(UserAdmin):
    inlines = (BasicInfoInline, AthleteInfoInline, )


admin.site.unregister(User)
admin.site.register(User, THUUserAdmin)
