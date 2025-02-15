from django.contrib import admin
from .models import Role, Secretary, BloodSecretary, Member


class MemberAdmin(admin.ModelAdmin):
    list_display = ('secretary', 'blood_secretary')
    search_fields = ('secretary__role', 'blood_secretary__role')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('role',)

# Register models with admin
admin.site.register(Role, RoleAdmin)
admin.site.register(Secretary)
admin.site.register(BloodSecretary)
admin.site.register(Member, MemberAdmin)
