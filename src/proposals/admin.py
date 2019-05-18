from django.contrib import admin

from .models import Proposal


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'added_on', 'updated_on', 'vote_count']
    list_filter = ['language']
    readonly_fields = [
        'author',
        'title',
        'abstract',
        'description',
        'audience_level',
        'added_on',
        'updated_on',
        'vote_count',
        'data',
        'data_history',
        'withdrawn',
    ]
    fieldsets = (
        (None, {'fields': ('title', 'author', 'abstract', 'description')}),
        ('Dates', {'fields': ('added_on', 'updated_on')}),
        ('Meta', {'fields': ('language', 'audience_level', 'vote_count', 'withdrawn')}),
        ('History', {'fields': ('data_history',)}),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProposalInline(admin.TabularInline):
    model = Proposal
