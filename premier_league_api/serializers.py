from rest_framework import serializers
from .models import Teams, Managers

class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ['name', 'abb']

class ManagersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Managers
        fields = ['id', 'first_name', 'last_name', 'age', 'nationality', 'team_name', 'contract_expiry', 'created_at', 'updated_at']

class FixturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Managers
        fields = ['id', 'game_week', 'date_time', 'stadium', 'home_team', 'away_team', 'home_score', 'away_score']