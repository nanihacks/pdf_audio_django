from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from PyPDF2 import PdfReader
import os



import pyttsx3
# import tempfile


def home(request):

    if request.method == "POST" and request.FILES.get("pdf_file"):

        text=''

        pdf_file = request.FILES.get("pdf_file")

        fs = FileSystemStorage()
        filename =  fs.save(pdf_file.name,pdf_file)
        file_path = fs.path(filename)

        file = open(file_path,'rb')

        reader = PdfReader(file)

        for page in reader.pages:
            page_text=page.extract_text()

            if page_text:
                
                text += page_text +'\n'

        
        audio_filename = filename.replace('.pdf','.mp3')
        audio_path = fs.path(audio_filename)
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # You can adjust speed
        engine.save_to_file(text, audio_path)
        engine.runAndWait()
        
        audio_url = fs.url(audio_filename)
        return render(request, "content.html",{'audio_url': audio_url})

    return render(request,"home.html")

