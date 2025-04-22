from django.db import models

class Customer(models.Model):
    userid = models.AutoField(primary_key=True)
    uservorname = models.CharField(max_length=255)  # ✅ Fixed name
    userstatus = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False  # Keep False to prevent Django from altering the DB
        db_table = 'tblbenutzer'
