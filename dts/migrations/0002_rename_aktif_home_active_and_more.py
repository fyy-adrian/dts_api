# Generated by Django 5.0.7 on 2024-08-06 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='home',
            old_name='aktif',
            new_name='active',
        ),
        migrations.RenameField(
            model_name='price',
            old_name='spesial',
            new_name='special',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='nama',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='pesan',
        ),
        migrations.RemoveField(
            model_name='home',
            name='gambar',
        ),
        migrations.RemoveField(
            model_name='partnership',
            name='gambar',
        ),
        migrations.RemoveField(
            model_name='partnership',
            name='nama',
        ),
        migrations.RemoveField(
            model_name='portofolio',
            name='gambar',
        ),
        migrations.RemoveField(
            model_name='price',
            name='fitur',
        ),
        migrations.RemoveField(
            model_name='price',
            name='harga',
        ),
        migrations.RemoveField(
            model_name='service',
            name='deskripsi',
        ),
        migrations.RemoveField(
            model_name='service',
            name='gambar',
        ),
        migrations.RemoveField(
            model_name='service',
            name='judul',
        ),
        migrations.AddField(
            model_name='contact',
            name='message',
            field=models.CharField(default='No Message', max_length=255),
        ),
        migrations.AddField(
            model_name='contact',
            name='name',
            field=models.CharField(default='No Name', max_length=255),
        ),
        migrations.AddField(
            model_name='home',
            name='image',
            field=models.ImageField(default='hero/default.jpg', max_length=255, upload_to='hero'),
        ),
        migrations.AddField(
            model_name='partnership',
            name='image',
            field=models.ImageField(default='partnership/default.jpg', max_length=255, upload_to='partnership'),
        ),
        migrations.AddField(
            model_name='partnership',
            name='name',
            field=models.CharField(default='No Name', max_length=255),
        ),
        migrations.AddField(
            model_name='portofolio',
            name='image',
            field=models.ImageField(default='portfolio/default.jpg', max_length=255, upload_to='portfolio'),
        ),
        migrations.AddField(
            model_name='price',
            name='features',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='price',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='service',
            name='description',
            field=models.CharField(default='No Description', max_length=255),
        ),
        migrations.AddField(
            model_name='service',
            name='image',
            field=models.ImageField(default='service/default.jpg', max_length=255, upload_to='service'),
        ),
        migrations.AddField(
            model_name='service',
            name='title',
            field=models.CharField(default='No Title', max_length=255),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.CharField(default='noemail@example.com', max_length=255),
        ),
        migrations.AlterField(
            model_name='price',
            name='level',
            field=models.CharField(default='No Level', max_length=255),
        ),
    ]
