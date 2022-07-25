# Generated by Django 3.2.9 on 2022-07-25 17:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Naam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam_nl', models.CharField(max_length=100)),
                ('naam_eng', models.CharField(max_length=100)),
                ('naam_wetenschappelijk', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=100)),
                ('type', models.IntegerField(choices=[(1, 'Standaard'), (2, 'Voorbeeld type')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='QuizSessieManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SoortScoreManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Familie',
            fields=[
                ('naam_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='application.naam')),
            ],
            bases=('application.naam',),
        ),
        migrations.CreateModel(
            name='Genus',
            fields=[
                ('naam_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='application.naam')),
                ('familie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.familie')),
            ],
            bases=('application.naam',),
        ),
        migrations.CreateModel(
            name='Klasse',
            fields=[
                ('naam_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='application.naam')),
            ],
            bases=('application.naam',),
        ),
        migrations.CreateModel(
            name='Soort',
            fields=[
                ('naam_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='application.naam')),
                ('moeilijkheidsgraad', models.IntegerField(choices=[(1, 'Zeer makkelijk'), (2, 'Makkelijk'), (3, 'Moeilijk'), (4, 'Zeer moeilijk')])),
                ('genus_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.genus')),
            ],
            bases=('application.naam',),
        ),
        migrations.CreateModel(
            name='QuizVraag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.quiz')),
                ('soort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.soort')),
            ],
        ),
        migrations.CreateModel(
            name='QuizSessie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuizAntwoord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('antwoord', models.CharField(max_length=100)),
                ('quizsessie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.quizsessie')),
                ('quizvraag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.quizvraag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SoortScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('soort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.soort')),
            ],
        ),
        migrations.CreateModel(
            name='LijktOp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soort1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='soort1', to='application.soort')),
                ('soort2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='soort2', to='application.soort')),
            ],
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.soort')),
            ],
        ),
        migrations.AddField(
            model_name='familie',
            name='klasse_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.klasse'),
        ),
    ]