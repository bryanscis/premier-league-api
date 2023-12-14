# Generated by Django 4.2.8 on 2023-12-14 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("premier_league_api", "0003_remove_teams_id_alter_teams_team_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="teams",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                default=1,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="teams", name="team_name", field=models.CharField(max_length=50),
        ),
    ]
