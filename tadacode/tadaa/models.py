
import numpy as np

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class MLModel(models.Model):
    name = models.CharField(max_length=120, default='')
    file_name = models.CharField(max_length=80, default='')
    url = models.URLField()
    public = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=datetime.now())
    owner = models.OneToOneField(User, null=True, blank=True)
    progress = models.PositiveIntegerField(default=0)
    notes = models.CharField(max_length=120)

    TBOX = 'tbox'
    ABOX = 'abox'
    EXTRACTION_CHOICES = (
        (TBOX, 'T-Box'),
        (ABOX, 'A-Box')
    )
    extraction_method = models.CharField(max_length=10, choices=EXTRACTION_CHOICES)

    NOT_STARTED = 'notstarted'
    RUNNING = 'running'
    STOPPED = 'stopped'
    COMPLETE = 'complete'
    STATE_CHOICES = (
        (RUNNING, 'Running'),
        (STOPPED, 'Stopped'),
        (COMPLETE, 'Complete'),
        (NOT_STARTED, 'Not Started Yet')
    )
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default=NOT_STARTED)

    def __unicode__(self):
        return str(self.id) + ") " + self.name


class PredictionRun(models.Model):
    mlmodel = models.ForeignKey(MLModel)
    name = models.CharField(max_length=120, default='')
    types = models.TextField(default='')
    public = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=datetime.now())
    owner = models.OneToOneField(User, null=True, blank=True)
    progress = models.PositiveIntegerField(default=0)
    notes = models.CharField(max_length=120)
    NOT_STARTED = 'notstarted'
    RUNNING = 'running'
    STOPPED = 'stopped'
    COMPLETE = 'complete'
    STATE_CHOICES = (
        (RUNNING, 'Running'),
        (STOPPED, 'Stopped'),
        (COMPLETE, 'Complete'),
        (NOT_STARTED, 'Not Started Yet')
    )
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default=NOT_STARTED)

    def __unicode__(self):
        return str(self.id) + ") " + self.name

    def add_memberships(self, u, file_column_list):
        """
        :param u: membership
        :param file_column_list:
        :param types:
        :return:
        """
        print "add_memberships> len of u is %d" % len(u)
        for idx, r in enumerate(u):
            print "membership %d" % idx
            m = Membership()
            m.prediction_run = self
            m.column_no = file_column_list[idx]["column_no"]
            m.file_name = file_column_list[idx]["file_name"]
            m = m.set_values(r)
            m.save()

    def set_types(self, types):
        self.types = ','.join(types)
        # self.save()

    def get_types(self):
        return self.types.split(',')


class Membership(models.Model):
    prediction_run = models.ForeignKey(PredictionRun)
    file_name = models.CharField(max_length=120, default='')
    column_no = models.PositiveIntegerField()
    values = models.TextField()

    def get_values_as_list_of_str(self):
        return self.values.split(',')

    def get_values_as_numpy(self):
        return np.array(self.get_values_as_list_of_str()).astype(np.float64)

    def set_values(self, vector):
        self.values = ",".join(["%1.5f" % cc for cc in vector])
        return self

    def __unicode__(self):
        return str(self.id) + ') ' + self.file_name + ', ' + str(self.column_no) + ' - ' + str(self.prediction_run.name)