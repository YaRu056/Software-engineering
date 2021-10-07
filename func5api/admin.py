from django.contrib import admin
from func5api.models import users,fix,manager

class usersAdmin(admin.ModelAdmin):
    list_display=('uid','name','student_number','created_time')
    
admin.site.register(users, usersAdmin)


class fixAdmin(admin.ModelAdmin):
    list_display=('student_number','cName','room','item',
                    'status','created_time')


admin.site.register(fix,fixAdmin)



class managerAdmin(admin.ModelAdmin):
    list_display=('name','student_number', 'aid')

admin.site.register(manager,managerAdmin)
