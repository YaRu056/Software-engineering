from django.db import models

class users(models.Model):
    uid = models.CharField(max_length=50, null=False, default='')
    name = models.CharField(max_length=20)
    student_number = models.CharField(max_length=10)
    created_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class fix(models.Model):
    items=(('未處理','未處理'), ('已處理','已處理'),)
    fid = models.CharField(max_length=50, null=False)
    cName = models.CharField(max_length=20, null=False)
    student_number =models.CharField(max_length=10,null=False)
    room =models.CharField(max_length=20,null=False)
    item = models.CharField(max_length=20,null=False)
    description = models.CharField(max_length=500,null=False)
    status =models.CharField(max_length=10, choices=items, default = '未處理')
    created_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.cName

class manager(models.Model):
    aid = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=20)
    student_number = models.CharField(max_length=10)
    def __str__(self):
        return self.name
