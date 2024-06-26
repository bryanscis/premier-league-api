from rest_framework import serializers
from .models import Teams, Managers, Fixtures, Players

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
        model = Fixtures
        fields = ['id', 'game_week', 'date_time', 'stadium', 'home_team', 'away_team', 'home_score', 'away_score', 'created_at', 'updated_at']

class PlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields = ['id', 'first_name', 'last_name', 'age', 'nationality', 'team_name', 'position', 'position', 'minutes_played', 'yellow_cards', 'red_cards', 'goals', 'assists', 'clean_sheets', 'total_apps', 'game_starts', 'sub_apps', 'created_at', 'updated_at']