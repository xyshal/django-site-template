from django.db import models

class TestModel(models.Model):
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zip_code = models.IntegerField()

    class Meta:
        ordering = ['state', 'address', 'zip_code']

    def __str__(self):
        return f"{self.address}, {self.state}, {self.zip_code}"

