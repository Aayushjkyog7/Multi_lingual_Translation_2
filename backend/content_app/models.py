from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'videos'
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'


class Moment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    moment_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'moments'
        verbose_name = 'Moment'
        verbose_name_plural = 'Moments'


class Podcast(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    podcast_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'podcasts'
        verbose_name = 'Podcast'
        verbose_name_plural = 'Podcasts'


class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    article_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'articles'
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

