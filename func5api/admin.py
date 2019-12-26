from django.contrib import admin
from func5api.models import users,fix

class usersAdmin(admin.ModelAdmin):
    list_display=('uid','name','student_number','created_time')
    
admin.site.register(users, usersAdmin)

class fixAdmin(admin.ModelAdmin):
    list_display=('student_number','cName','room','item',
                    'status','created_time')


admin.site.register(fix,fixAdmin)
