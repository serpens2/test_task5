from django.db import models

class Quote(models.Model):
    text = models.CharField(max_length=1000, null=False)
    source = models.CharField(max_length=50,null=False)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    weight_choices = [
        (1,"маленький"),
        (2,"средний"),
        (3,"большой")
    ]
    weight = models.IntegerField(choices=weight_choices, default=2)