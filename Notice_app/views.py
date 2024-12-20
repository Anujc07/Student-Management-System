from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *


def Add_Notice(request):
    if request.method == "POST":
        title = request.POST['title']
        notice_file = request.FILES['notice_file']
        date_of_notice = request.POST['date_of_notice']
        published_by = request.POST['published_by']
        description = request.POST.get('description', '')
        audience_type = request.POST['audience_type']
        specific_semester = request.POST.get('specific_semester', '')
        specific_year = request.POST.get('specific_year', '')

        notice = Notice.objects.create(
            title=title,
            notice_file=notice_file,
            date_of_notice=date_of_notice,
            published_by=published_by,
            description=description,
            audience_type=audience_type,
            specific_semester=specific_semester,
            specific_year=specific_year
        )
        notice.save()
        messages.success(request, "Notice added successfully!")
        return redirect('./Add-Books')

    return render(request, 'Notice/Add_Notice.html')



def Notice_List(request):
    title = request.GET.get('title', '')
    date = request.GET.get('date', '')

    notices = Notice.objects.all()

    if title:
        notices = notices.filter(title__icontains=title)
    if date:
        notices = notices.filter(date_of_notice=date)

    return render(request, 'Notice/Notice_List.html', {'notice_list': notices})