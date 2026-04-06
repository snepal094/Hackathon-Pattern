from django.db import models

# Create your models here.

class tablelog(models.Model):
    filename = models.CharField(max_length=500, unique=True)
    client = models.CharField(max_length=100)
    regex = models.CharField(max_length=500)

class generated_patterns(models.Model):
    filename = models.CharField(max_length=500, unique = True)
    client = models.CharField(max_length=100)
    regex = models.CharField(max_length=500)


class pattern_layout_mapping(models.Model):
    payor = models.CharField(max_length=100)
    layout_id = models.IntegerField() 
    datatype = models.CharField(max_length=100)
    employergroup = models.CharField(max_length=100)
    layouttype = models.CharField(max_length=100)
    pattern = models.CharField(max_length=500)
    addeddate = models.DateField()    
    modifieddate = models.DateField(null=True, blank=True) 