from django.contrib import admin

from .models import ConfirmationState


@admin.register(ConfirmationState)
class ConfirmationStateAdmin(admin.ModelAdmin):
    list_display = 'id', 'code', 'is_confirmed', 'created_at', 'updated_at',
    date_hierarchy = 'created_at'
    list_filter = 'is_confirmed', 'created_at', 'updated_at'
