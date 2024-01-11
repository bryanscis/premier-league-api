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
        unique_together = [("first_name", "last_name", "nationality")]

    def __str__(self):
        return f'{self.first_name} | {self.last_name} | {self.age} | {self.nationality} | {self.team_name} | {self.contract_expiry} '
    
class Fixtures(models.Model):
    game_week = models.IntegerField()
    date_time = models.DateTimeField()
    stadium = models.CharField(max_length=50)
    home_team = models.ForeignKey("Teams", on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey("Teams", on_delete=models.CASCADE, related_name='away_team')
    home_score = models.IntegerField(null=True)
    away_score = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = [("game_week", "home_team", "away_team")]

    def __str__(self):
        return f'Week {self.game_week}: {self.home_team} {self.home_score} - {self.away_score} {self.away_team} at {self.stadium} on {self.date_time}'
    
class Players(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=False, blank=True)
    age = models.IntegerField()
    nationality = models.CharField(max_length=100)
    team_name = models.ForeignKey("Teams", on_delete=models.CASCADE)
    position = models.CharField(max_length=20)
    minutes_played = models.IntegerField()
    yellow_cards = models.IntegerField()
    red_cards = models.IntegerField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    clean_sheets = models.IntegerField()
    total_apps = models.IntegerField()
    game_starts = models.IntegerField()
    sub_apps = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = [("first_name", "last_name", "nationality", "team_name")]

    def __str__(self):
        return f'{self.first_name} {self.last_name} : {self.team_name}'