from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class LoadenedEntitiy(models.Model):
    link = models.CharField(max_length=225)
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    entity_type = models.CharField(max_length=1,choices=(('C','channel'),
                                                          ('G','group'),
                                                        ))
    label = models.CharField(max_length=2,choices=(('to','post_to'),('fr','from')))
    date = models.DateTimeField(default= timezone.now)
    
    def __str__(self):
        return self.link