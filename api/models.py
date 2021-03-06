from django.db import models
from django.contrib.auth.models import User

class Conference(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Member(models.Model):
    name = models.CharField(max_length=63)
    surname = models.CharField(max_length=63)
    middlename = models.CharField(max_length=63)
    email = models.EmailField(max_length=127)
    city = models.CharField(max_length=127)
    uni = models.CharField(max_length=127)
    course = models.CharField(max_length=127)
    with_topic = models.BooleanField(default=False)
    topic = models.CharField(max_length=511)
    approved = models.BooleanField(default=None, null=True)

    conf = models.ForeignKey(Conference, on_delete=models.CASCADE)

    def __repr__(self):
        return "<Member {} {}: {} {}>".format(self.id, ("with topic" if self.topic else ""), self.name, self.surname)

    def to_dict(self):
        return {
                "id": self.id,
                "name": self.surname + " " + self.name + " " + self.middlename,
                "email": self.email,
                "city": self.city,
                "uni": self.uni,
                "course": self.course,
                "with_topic": self.with_topic,
                "topic": self.topic,
                "approved": self.approved,
            }