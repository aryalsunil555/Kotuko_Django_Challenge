from pyexpat import model
from django.contrib import admin
from exam.models import ToDOList, ToDouser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class UserModelAdmin(BaseUserAdmin):

    list_display = ('id','email', 'fullname', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('fullname',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
  
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email','id')
    filter_horizontal = ()


admin.site.register(ToDouser, UserModelAdmin)

class TodoListModel(UserModelAdmin):
 

   
    list_display = ('id','name', 'description', 'uploaded_by')
    list_filter = ('name','uploaded_by')
    fieldsets = (
        ('User Credentials', {'fields': ('uploaded_by',)}),
        ('TodoList Info info', {'fields': ('name','description','image','deadline')}),
       
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'description'),
        }),
    )
    search_fields = ('name',)
    ordering = ('name','creation_date')
    filter_horizontal = ()

admin.site.register(ToDOList, TodoListModel)