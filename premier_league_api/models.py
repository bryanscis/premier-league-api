from django.db import models

class Teams(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    abb = models.CharField(max_length=3)

    def __str__(self):
        return f'{self.name}'

class Managers(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    nationality = models.CharField(max_length=100)
    team_name = models.ForeignKey("Teams", on_delete=models.CASCADE)
    contract_expiry = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ["first_name", "last_name", "nationality"]

    def __str__(self):
        return f'{self.first_name} | {self.last_name} | {self.age} | {self.nationality} | {self.team_name} | {self.contract_expiry} '