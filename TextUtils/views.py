from django.shortcuts import HttpResponse, render
from django.http import FileResponse
from django.utils.html import escape
import string
import re
from langdetect import detect
from textblob import TextBlob
from django.core.files.storage import FileSystemStorage
from io import BytesIO
import pyttsx3
import os
from django.conf import settings

def serve_audio(request, filename):
    file_path = os.path.join(settings.STATIC_ROOT, filename)
    return FileResponse(open(file_path, 'rb'), content_type='audio/mp3')

# Create your views here.
def index(request):
    return render(request, 'myapp/index.html')

def analyse(request):
    djtext = request.GET.get('text', 'default')
    removePunc = request.GET.get('removePunc', 'off')
    fullcaps = request.GET.get('fullcaps', 'off')
    lowercase = request.GET.get('lowercase', 'off')
    titlecase = request.GET.get('titlecase', 'off')
    newlineremover = request.GET.get('newlineremover', 'off')
    extraspaceremover = request.GET.get('extraspaceremover', 'off')
    charcount = request.GET.get('charcount', 'off')
    wordcount = request.GET.get('wordcount', 'off')
    sentcount = request.GET.get('sentcount', 'off')
    reversetext = request.GET.get('reversetext', 'off')
    searchreplace = request.GET.get('searchreplace', 'off')
    removestopwords = request.GET.get('removestopwords', 'off')
    sentimentanalysis = request.GET.get('sentimentanalysis', 'off')
    languagedetection = request.GET.get('languagedetection', 'off')
    readabilityscore = request.GET.get('readabilityscore', 'off')
    loremipsum = request.GET.get('loremipsum', 'off')
    texttospeech = request.GET.get('texttospeech', 'off')
    speechtotext = request.GET.get('speechtotext', 'off')

    analysedText = djtext
    purpose = []

    if removePunc == "on":
        analysedText = ''.join([char for char in analysedText if char not in string.punctuation])
        purpose.append("Removed Punctuation")

    if fullcaps == "on":
        analysedText = analysedText.upper()
        purpose.append("Converted to UPPERCASE")

    if lowercase == "on":
        analysedText = analysedText.lower()
        purpose.append("Converted to lowercase")

    if titlecase == "on":
        analysedText = analysedText.title()
        purpose.append("Converted to Title Case")

    if newlineremover == "on":
        analysedText = analysedText.replace('\n', '').replace('\r', '')
        purpose.append("Removed New Lines")

    if extraspaceremover == "on":
        analysedText = ' '.join(analysedText.split())
        purpose.append("Removed Extra Spaces")

    if charcount == "on":
        char_count = len(analysedText)
        purpose.append(f"Character Count: {char_count}")

    if wordcount == "on":
        word_count = len(analysedText.split())
        purpose.append(f"Word Count: {word_count}")

    if sentcount == "on":
        sent_count = len(re.split(r'[.!?]+', analysedText)) - 1
        purpose.append(f"Sentence Count: {sent_count}")

    if reversetext == "on":
        analysedText = analysedText[::-1]
        purpose.append("Reversed Text")

    if searchreplace == "on":
        search = request.GET.get('searchtext', '')
        replace = request.GET.get('replacetext', '')
        analysedText = analysedText.replace(search, replace)
        purpose.append(f"Replaced '{search}' with '{replace}'")

    if removestopwords == "on":
        stopwords = set()
        try:
            with open('stopwords.txt') as f:
                stopwords = set(f.read().split())
        except FileNotFoundError:
            purpose.append("Stop Words file not found")
        analysedText = ' '.join([word for word in analysedText.split() if word.lower() not in stopwords])
        purpose.append("Removed Stop Words")

    if sentimentanalysis == "on":
        blob = TextBlob(analysedText)
        sentiment = blob.sentiment
        purpose.append(f"Sentiment Analysis: Polarity={sentiment.polarity}, Subjectivity={sentiment.subjectivity}")

    if languagedetection == "on":
        language = detect(analysedText)
        purpose.append(f"Language Detection: {language}")

    if readabilityscore == "on":
        # Implement a simple readability score like Flesch-Kincaid
        words = len(analysedText.split())
        sentences = len(re.split(r'[.!?]+', analysedText)) - 1
        syllables = sum(len([char for char in word if char in 'aeiou']) for word in analysedText.split())
        readability = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
        purpose.append(f"Readability Score: {readability:.2f}")

    if loremipsum == "on":
        analysedText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        purpose.append("Generated Lorem Ipsum")

    if texttospeech == "on":
        engine = pyttsx3.init()
        engine.save_to_file(analysedText, 'output.mp3')
        engine.runAndWait()
        purpose.append("Converted Text to Speech")

    if speechtotext == "on":
        # Placeholder for speech to text functionality
        purpose.append("Converted Speech to Text")

    params = {'purpose': ' | '.join(purpose), 'analysedText': analysedText}
    return render(request, 'myapp/analyse.html', params)

def capitaliseFirst(request):
    return HttpResponse('<h1>hola2</h1>')
