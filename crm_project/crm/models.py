from django.db import models

class Customer(models.Model):
    userid = models.AutoField(primary_key=True, db_column='pers#nr#')  # Field name made lowercase
    uservorname = models.CharField(max_length=255, db_column='firstname')  # Field name made lowercase
    userstatus = models.CharField(max_length=255, blank=True, db_column='status')
    useremail = models.CharField(max_length=255,db_column='email')

    class Meta:
        managed = False  # Keep False to prevent Django from altering the DB
        db_table = 'pslemployees'
