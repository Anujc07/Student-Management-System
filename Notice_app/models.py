from django.db import models


class Notice(models.Model):

    title = models.CharField(max_length=200, verbose_name="Notice Title")
    notice_file = models.FileField(upload_to='notices/', verbose_name="Notice File (Image/PDF)")
    date_of_notice = models.DateField(verbose_name="Date of Notice")
    published_by = models.CharField(max_length=100, verbose_name="Published By")
    description = models.TextField(blank=True, verbose_name="Description")
    audience_type = models.CharField(max_length=20, default='all', verbose_name="Audience Type")
    specific_semester = models.CharField(max_length=50, blank=True, null=True, verbose_name="Specific Semester (if any)")
    specific_year = models.CharField(max_length=50, blank=True, null=True, verbose_name="Specific Year (if any)")

    def __str__(self):
        return self.title

