from django.db import models


class RemoteObject(models.Model):
    remote_id = models.IntegerField(unique=True)


class Object(models.Model):
    remote_object = models.ForeignKey(RemoteObject, to_field="remote_id", db_constraint=False, on_delete=models.DO_NOTHING, null=True, blank=True)
