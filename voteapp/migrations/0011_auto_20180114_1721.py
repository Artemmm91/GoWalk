# Generated by Django 2.0 on 2018-01-14 17:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('voteapp', '0010_merge_20180114_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='Polls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('text', models.CharField(max_length=400)),
                ('is_checkbox', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='votings',
            name='user',
        ),
        migrations.AlterField(
            model_name='options',
            name='voting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='voteapp.Polls'),
        ),
        migrations.DeleteModel(
            name='Votings',
        ),
    ]