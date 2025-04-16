from django.db import models

class CodeGround(models.Model):
    question = models.TextField()
    visible_testcases = models.JSONField(default=list)
    hidden_testcases = models.JSONField(default=list)

    def __str__(self):
        return self.question[:50]