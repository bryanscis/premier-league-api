from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
from .models import Teams, Managers
from .serializers import TeamsSerializer, ManagersSerializer, FixturesSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests, json, datetime
import premier_league_api.constants as CONSTANTS
from bs4 import BeautifulSoup

@api_view(['POST'])
def add_managers(request):

    if request.method == 'POST':
        response = requests.get("https://www.transfermarkt.us/premier-league/trainer/pokalwettbewerb/GB1", headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(response.content, 'html.parser').find('table', {'class':'items'}).find_all('tr')[1:]
        all_managers = {}
        # Split manager information
        for manager in soup:
            manager_name = manager.get_text(separator = "|").split('|')[1]
            manager_nationality = manager.find( 'img', {'class': 'flaggenrahmen'})['title']
            manager_team = manager.find( 'img', {'class': 'tiny_wappen'})['title']
            all_managers[manager_name] = manager.get_text(separator = "|").split('|')[2:] + [ CONSTANTS.TEAMS[manager_team], manager_nationality]
        for manager, manager_info in all_managers.items():
            manager_info[2] = None if manager_info[2] == '?' else manager_info[2]
            manager_name = manager.split(" ", 1)
            serializer = ManagersSerializer(data={'first_name': manager_name[0], 'last_name':manager_name[1], 'age':manager_info[0], 'nationality': manager_info[5], 'team_name':manager_info[4], 'contract_expiry': manager_info[2], 'created_at': datetime.datetime.now(), 'updated_at': datetime.datetime.now()})
            # Save data if no errors
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except IntegrityError:
                return Response(data={serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def add_fixtures(request):

    if request.method == 'POST':
        response = requests.get('https://fixturedownload.com/feed/json/epl-2023').json()
        for match in response:
            match['HomeTeam'] = CONSTANTS.TEAMSFIXTURES[match['HomeTeam']]
            match['AwayTeam'] = CONSTANTS.TEAMSFIXTURES[match['AwayTeam']]
            match['DateUtc'] = match['DateUtc'][:-1] + '+00'
            serializer = FixturesSerializer(data={'game_week': match['RoundNumber'], 'date_time': match['DateUtc'], 'stadium': match['Location'], 'home_team': match['HomeTeam'], 'away_team': match['AwayTeam'], 'home_score': match['HomeTeamScore'], 'away_score': match['AwayTeamScore'],'created_at': datetime.datetime.now(), 'updated_at': datetime.datetime.now()})
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except IntegrityError:
                return Response(data={serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
