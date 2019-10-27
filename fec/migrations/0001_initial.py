# Generated by Django 2.2.6 on 2019-10-27 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('office', models.CharField(choices=[('H', 'House'), ('S', 'Senate'), ('P', 'President')], max_length=1, null=True)),
                ('party', models.CharField(max_length=3, null=True)),
                ('state', models.CharField(max_length=2, null=True)),
                ('district', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('committee_id', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('candidate', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='fec.Candidate')),
            ],
        ),
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, null=True)),
                ('zip', models.CharField(max_length=9, null=True)),
                ('employer', models.CharField(max_length=38, null=True)),
                ('occupation', models.CharField(max_length=38, null=True)),
                ('committee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='fec.Committee')),
            ],
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='source_connections', to='fec.Candidate')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='target_connections', to='fec.Candidate')),
            ],
        ),
        migrations.AddIndex(
            model_name='contribution',
            index=models.Index(fields=['name', 'zip', 'employer', 'occupation'], name='fec_contrib_name_2d902d_idx'),
        ),
    ]
