import json
#import logging
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from dtb.settings import DEBUG
from tgbot.dispatcher import process_telegram_event, webhook
from resume.static.text.static_text import work_list, skills_list, about_me


def index(request):
    return JsonResponse({"error": "sup hacker"})

class ErrorView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'ERROR':'Sorry. This page is under development now'})

class ResumeView(View):
    # WARNING: if fail - Telegram webhook will be delivered again. 
    # Can be fixed with async celery task execution
    def post(self, request, *args, **kwargs):


        if DEBUG:
            webhook(json.loads(request.body))
            # process_telegram_event(json.loads(request.body))
        else:  
            # Process Telegram event in Celery worker (async)
            # Don't forget to run it and & Redis (message broker for Celery)! 
            # Read Procfile for details
            # You can run all of these services via docker-compose.yml
            webhook(json.loads(request.body))
            # process_telegram_event.delay(json.loads(request.body))

        return JsonResponse({"ok": "POST request processed"})
    
    def get(self, request, *args, **kwargs):  # for debug

        return render(request, 'resume_page.html', {'work_list':work_list, 'skill_list':skills_list, 'about_me':about_me})
