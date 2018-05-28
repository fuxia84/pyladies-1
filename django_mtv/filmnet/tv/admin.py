from django.contrib import admin

from . import models


class ProgramInline(admin.StackedInline):
    model = models.Program
    extra = 0


@admin.register(models.Station)
class StationAdmin(admin.ModelAdmin):
    inlines = [ProgramInline]


@admin.register(models.Program)
class ProgramAdmin(admin.ModelAdmin):
    pass
