from django.contrib import admin

from roommanage.models import Classroom, bookClassroom,Routine

# Register your models here.
class RoutineAdmin(admin.ModelAdmin):
    MAX_OBJECTS = 1
    print("tera routine",Routine.objects.all()[0].routine)
    def has_add_permission(self, request):
        if self.model.objects.count() >= self.MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

admin.site.register(Routine)
admin.site.register(Classroom)
admin.site.register(bookClassroom)