from django.shortcuts import render
from django.http import HttpResponse,request,StreamingHttpResponse
import mysql.connector
from django.views.decorators import gzip
import cv2
import threading
import logging
import os
import shutil
import zipfile
from django.conf import settings
from decouple import config
from googleapiclient.discovery import build
import urllib,random
from urllib import request, error
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from googleapiclient.discovery import build
from pytube import YouTube
from pydub import AudioSegment
import re

# Create your views here.

def index(request):
    return render(request, 'audiomashup/index.html')

def get_youtube_stream(video_id):
    api_key = config('YOUTUBE_API_KEY')
    youtube = build("youtube", "v3", developerKey=api_key)
    video = youtube.videos().list(part="contentDetails", id=video_id).execute()
    duration = video["items"][0]["contentDetails"]["duration"]
    return duration

def mixer(request):
    if request.method == 'POST':
        singer_name = request.POST.get('singer')
        num_videos = int(request.POST.get('num'))
        duration = int(request.POST.get('dur'))
        email = request.POST.get('email')
        X = singer_name.lower().replace(" ", "") + "videosongs"

        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + X)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        l = len(video_ids)
        url = []
        for i in range(num_videos):
            url.append("https://www.youtube.com/watch?v=" + video_ids[random.randint(0, l - 1)])

        final_aud = AudioSegment.empty()
        for i in range(num_videos):
            yt = YouTube(url[i])
            yt.streams.filter(only_audio=True).first().download(filename=f'Audio-{i}.mp3')
            print(f"\n\t\t\t\tAudio-{i} Downloaded successfully✅")
            aud_file = os.path.join(os.getcwd(), f"Audio-{i}.mp3")
            file1 = AudioSegment.from_file(aud_file)
            extracted_file = file1[:duration * 1000]
            final_aud += extracted_file

        output_filename = f'Mashup_{singer_name}.mp3'
        final_aud.export(output_filename, format="mp3")

        # Create a zip file containing the generated mashup
        zip_filename = f'Mashup_{singer_name}.zip'
        with zipfile.ZipFile(zip_filename, 'w') as zip_file:
            zip_file.write(output_filename, arcname=output_filename)

        # Send an email with the zip file as an attachment
        subject = 'Audio Mashup'
        message = f'Please find attached the mashup created for {singer_name}.'
        from_email = 'nchadha_be21@thapar.edu'
        recipient_list = [email]

        # send_mail(subject, message, from_email, recipient_list, fail_silently=False,
        #           html_message=None, attach=[(zip_filename, open(zip_filename, 'rb').read())])
        email_message = EmailMessage(
        subject,
        message,
        from_email,
        recipient_list,
    )
        email_message.attach_file(zip_filename)
        email_message.send(fail_silently=False)

        # Clean up: Delete the temporary files and zip file
        os.remove(output_filename)
        os.remove(zip_filename)
        os.remove(aud_file)
        # Provide the success message to be displayed in the template
        success_message = f"Mashup Sent successfully"
        error_message=f"Mashup not Sent"

        # Pass the message as a context variable
        context = {'message': success_message}
        context1 = {'message': error_message}

        # Render the template with the provided context
        return render(request, 'audiomashup/success.html', context)

    return render(request, 'audiomashup/success.html', context1)
