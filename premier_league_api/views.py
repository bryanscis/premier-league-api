from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
from django.utils import timezone
from .models import Teams, Managers, Fixtures, Players
from .serializers import TeamsSerializer, ManagersSerializer, FixturesSerializer, PlayersSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import requests, json, datetime
import premier_league_api.constants as CONSTANTS
from bs4 import BeautifulSoup

@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def add_managers(request):
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
            if request.method == 'POST':
                serializer = ManagersSerializer(data={'first_name': manager_name[0], 'last_name':manager_name[1], 'age':manager_info[0], 'nationality': manager_info[5], 'team_name':manager_info[4], 'contract_expiry': manager_info[2], 'created_at': timezone.now(), 'updated_at': timezone.now()})
                # Save data if no errors
                try:
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                except IntegrityError:
                    return Response(data={serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            elif request.method == 'PUT': 
                try:    
                    Managers.objects.filter(team_name=manager_info[4]).update(first_name=manager_name[0], last_name=manager_name[1], age=manager_info[0], nationality= manager_info[5], team_name=manager_info[4], contract_expiry= manager_info[2], updated_at=timezone.now())
                except:
                    return Response(data={serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def add_fixtures(request):
    response = requests.get('https://fixturedownload.com/feed/json/epl-2023').json()
    for match in response:
        match['HomeTeam'] = CONSTANTS.TEAMSFIXTURES[match['HomeTeam']]
        match['AwayTeam'] = CONSTANTS.TEAMSFIXTURES[match['AwayTeam']]
        match['DateUtc'] = match['DateUtc'][:-1] + '+00'
        if request.method == 'POST':
            serializer = FixturesSerializer(data={'game_week': match['RoundNumber'], 'date_time': match['DateUtc'], 'stadium': match['Location'], 'home_team': match['HomeTeam'], 'away_team': match['AwayTeam'], 'home_score': match['HomeTeamScore'], 'away_score': match['AwayTeamScore'],'created_at': timezone.now(), 'updated_at': timezone.now()})
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except IntegrityError:
                return Response(data={serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'PUT':
            try:
                Fixtures.objects.filter(game_week=match['RoundNumber'], home_team=match['HomeTeam'], away_team=match['AwayTeam']).update(date_time= match['DateUtc'], home_score= match['HomeTeamScore'], away_score= match['AwayTeamScore'], updated_at=timezone.now())
            except:
                return Response(data={serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_players(request):

    if request.method == 'POST':
        response = requests.get("https://www.footballcritic.com/json/competition-player-stats.php?uid=68731")
        json_string = json.loads(json.dumps(response.json(), indent = 4, sort_keys=True))
        for i, ps in enumerate(json_string[0], 1):
            serializer = PlayersSerializer()
            if type(ps) == list:
                first_name, *last_name = str(ps[2]).split(' ', 1)
                last_name = last_name[0] if last_name else ''
                position = str(ps[13]).replace(" ", "").replace("<BR/>", "")
                age, nationality, team, minutes, yellow, red, goals, assists, c_sheets, apps, starts, sub_apps = int(ps[0]), str(ps[3]), str(ps[8]), int(ps[17]), int(ps[18]), int(ps[19]), int(ps[20]), int(ps[21]), int(ps[22]), int(ps[25]), int(ps[26]), int(ps[27])
                serializer = PlayersSerializer(data= {'first_name': first_name, 'last_name': last_name, 'age': age, 'nationality': nationality, 'team_name': team, 'position': position, 'minutes_played': minutes, 'yellow_cards':yellow, 'red_cards':red, 'goals': goals, 'assists': assists, 'clean_sheets': c_sheets, 'total_apps': apps, 'game_starts': starts, 'sub_apps':sub_apps})
            elif type(ps) == dict:
                first_name, *last_name = str(ps['2']).split(' ', 1)
                last_name = last_name[0] if last_name else ''
                position = str(ps['13']).replace(" ", "").replace("<BR/>", "")
                age, nationality, team, minutes, yellow, red, goals, assists, c_sheets, apps, starts, sub_apps = int(ps['0']), str(ps['3']), str(ps['8']), int(ps['17']), int(ps['18']), int(ps['19']), int(ps['20']), int(ps['21']), int(ps['22']), int(ps['25']), int(ps['26']), int(ps['27'])
                serializer = PlayersSerializer(data= {'first_name': first_name, 'last_name': last_name, 'age': age, 'nationality': nationality, 'team_name': team, 'position': position, 'minutes_played': minutes, 'yellow_cards':yellow, 'red_cards':red, 'goals': goals, 'assists': assists, 'clean_sheets': c_sheets, 'total_apps': apps, 'game_starts': starts, 'sub_apps':sub_apps})
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except IntegrityError:
                return Response(data={serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def get_teams(request):

    if request.method == 'GET':
        try:
            teams, serializer = None, None
            abb = request.GET.get('abb')
            if abb:
                teams = Teams.objects.get(abb=abb)
                serializer = TeamsSerializer(teams)
            else:
                teams = Teams.objects.all().order_by('name')
                serializer = TeamsSerializer(teams, many=True)
            return JsonResponse({'teams': serializer.data}, status=200)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def get_managers(request):

    if request.method == 'GET':
        last_name, abb = request.GET.get('last_name'),request.GET.get('abb')
        try:
            managers, serializer = None, None
            if last_name:
                managers = Managers.objects.get(last_name=last_name )
                serializer = ManagersSerializer(managers)
            elif abb:
                managers = Managers.objects.get(team_name_id=Teams.objects.get(abb=abb).name)
                serializer = ManagersSerializer(managers)
            else:
                managers = Managers.objects.all().order_by('team_name_id')
                serializer = ManagersSerializer(managers, many=True)
            return JsonResponse({'managers': serializer.data}, status=200)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def get_fixtures(request):

    if request.method == 'GET':
        played, abb = request.GET.get('played'), request.GET.get('abb')
        try:
            fixtures, serializer = None, None
            if played:
                if played == 'False':
                    fixtures = Fixtures.objects.exclude(home_score__isnull=False, away_score__isnull=False).order_by('date_time')
                elif played == 'True':
                    fixtures = Fixtures.objects.exclude(home_score__isnull=True, away_score__isnull=True).order_by('date_time')
                serializer = FixturesSerializer(fixtures, many=True)
            elif abb:
                fixtures = Fixtures.objects.filter(home_team_id=Teams.objects.get(abb=abb).name) | Fixtures.objects.filter(away_team_id=Teams.objects.get(abb=abb).name)
                serializer = FixturesSerializer(fixtures, many=True)
            else:
                fixtures = Fixtures.objects.all().order_by('date_time')
                serializer = FixturesSerializer(fixtures, many=True)
            return JsonResponse({'fixtures': serializer.data}, status=200)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_players(request):

    if request.method == 'GET':
        last_name = request.GET.get('last_name')
        try:
            players, serializer = None, None
            if last_name:
                players = Players.objects.filter(last_name=last_name)
                serializer = PlayersSerializer(players, many=True)
            else:
                players = Players.objects.all().order_by('id')
                serializer = PlayersSerializer(players, many=True)
            return JsonResponse({'players': serializer.data}, status=200)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)