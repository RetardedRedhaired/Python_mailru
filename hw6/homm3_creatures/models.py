from django.db import models


class Creature(models.Model):
    name = models.CharField('Названия существа', max_length=128, null=False)
    level = models.IntegerField('Уровень существа', null=False)
    descr = models.TextField('писание существа', null=True)
