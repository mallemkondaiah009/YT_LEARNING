from django.db import models

class CodingProblem(models.Model):
    problem_id = models.IntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    problem = models.TextField()
    input_desc = models.TextField()
    output_desc = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['problem_id']

class TestCase(models.Model):
    problem = models.ForeignKey(CodingProblem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.JSONField(null=True, blank=True)  # Allow null for debugging
    output_data = models.JSONField(null=True, blank=True)  # Allow null for debugging

    def __str__(self):
        return f"Test case for {self.problem.title}"