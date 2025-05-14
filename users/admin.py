from django.contrib import admin


# Register your models here.
@admin.register
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "city", "avatar", "tg_nick")
