from django.db import models

class Customer(models.Model):
    userid = models.AutoField(primary_key=True, db_column='userid')  # Field name made lowercase
    uservorname = models.CharField(max_length=255, db_column='uservorname')  # Field name made lowercase
    userstatus = models.CharField(max_length=255, blank=True, db_column='usernachname')
    useremail = models.CharField(max_length=255,db_column='email')

    class Meta:
        managed = False  # Keep False to prevent Django from altering the DB
        db_table = 'tblbenutzer'  # Table name in the database
