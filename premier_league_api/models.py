from django.db import models

class Teams(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'

class Managers(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    nationality = models.CharField(max_length=100)
    team = models.ForeignKey("Teams", on_delete=models.CASCADE)
    contract_expiry = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} | {self.last_name} | {self.age} | {self.nationality} | {self.team} | {self.contract_expiry} '