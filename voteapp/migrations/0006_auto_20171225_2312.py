# Generated by Django 2.0 on 2017-12-25 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voteapp', '0005_auto_20171225_2308'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='voteapp.Users')),
            ],
        ),
        migrations.AlterField(
            model_name='votings',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='voteapp.Users'),
        ),
        migrations.RenameModel(
            old_name='Variant',
            new_name='Variants',
        ),
        migrations.AddField(
            model_name='votes',
            name='variant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='voteapp.Variants'),
        ),
    ]
