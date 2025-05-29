from materials.models import Course
from django.contrib import admin


class CourseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Course, CourseAdmin)
