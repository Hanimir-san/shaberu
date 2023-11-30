import io
import scipy
import soundfile
import os
import tempfile
import re

from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.views.generic.base import TemplateView

from django.contrib.auth import views as auth_views

from home.forms import LoginForm, RegistrationForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm

from gpt4all import GPT4All
import speech_recognition as sr
from transformers import AutoProcessor, BarkModel
from speech_recognition.exceptions import UnknownValueError

from language.models import LanguageModel


# Create your views here.


# Authentication
def registration(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print('Account created successfully!')
      return redirect('/accounts/login/')
    else:
      print("Registration failed!")
  else:
    form = RegistrationForm()
  
  context = {'form': form}
  return render(request, 'accounts/sign-up.html', context)

class UserLoginView(auth_views.LoginView):
  template_name = 'accounts/sign-in.html'
  form_class = LoginForm
  success_url = '/'

class UserPasswordResetView(auth_views.PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(auth_views.PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm

def user_logout_view(request):
  logout(request)
  return redirect('/accounts/login/')


# Pages
def index(request):
  return render(request, 'pages/index.html')

def contact_us(request):
  return render(request, 'pages/contact-us.html')

def about_us(request):
  return render(request, 'pages/about-us.html')

def author(request):
  return render(request, 'pages/author.html')


# Sections
def presentation(request):
  return render(request, 'sections/presentation.html')
  
def page_header(request):
  return render(request, 'sections/page-sections/hero-sections.html')

def features(request):
  return render(request, 'sections/page-sections/features.html')

def navbars(request):
  return render(request, 'sections/navigation/navbars.html')

def nav_tabs(request):
  return render(request, 'sections/navigation/nav-tabs.html')

def pagination(request):
  return render(request, 'sections/navigation/pagination.html')

def forms(request):
  return render(request, 'sections/input-areas/forms.html')

def inputs(request):
  return render(request, 'sections/input-areas/inputs.html')

def avatars(request):
  return render(request, 'sections/elements/avatars.html')

def badges(request):
  return render(request, 'sections/elements/badges.html')

def breadcrumbs(request):
  return render(request, 'sections/elements/breadcrumbs.html')

def buttons(request):
  return render(request, 'sections/elements/buttons.html')

def dropdowns(request):
  return render(request, 'sections/elements/dropdowns.html')

def progress_bars(request):
  return render(request, 'sections/elements/progress-bars.html')

def toggles(request):
  return render(request, 'sections/elements/toggles.html')

def typography(request):
  return render(request, 'sections/elements/typography.html')

def alerts(request):
  return render(request, 'sections/attention-catchers/alerts.html')

def modals(request):
  return render(request, 'sections/attention-catchers/modals.html')

def tooltips(request):
  return render(request, 'sections/attention-catchers/tooltips-popovers.html')


class ChatMainAudioAjax(View):
    
    def post(self, request, *args, **kwargs):
        
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest': 
            return HttpResponseBadRequest()
        
        input = request.FILES.get('chat-user-audio')
        file = input.file
        file.seek(0)

        # Write data to temporary file as wav
        data, samplerate = soundfile.read(file)
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file_obj:
          tmp_name = tmp_file_obj.name
        soundfile.write(
            tmp_name, 
            data, 
            samplerate=samplerate, 
            subtype='PCM_16', 
            format='wav'
        )

        # Send data to speech recognizer
        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_name) as source:
          data = recognizer.record(source)
        
        try:
          output = recognizer.recognize_google(data)
        except UnknownValueError:
          output = "Sorry, we couldn't hear what you said!"

        data = {'result': output}
        return JsonResponse(data)


class ChatMainAjax(View):
    
    def post(self, request, *args, **kwargs):
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest': 
            return HttpResponseBadRequest()
        input = request.POST.get('chat-user-resp')
        print(input)

        # Text generation
        model_record = LanguageModel.objects.filter(type=LanguageModel.CHOICE_GPT4ALL, file__isnull=False, is_default=True)
        if not model_record.exists():
          model_record = LanguageModel.objects.filter(type=LanguageModel.CHOICE_GPT4ALL, file__isnull=False)
        if not model_record.exists():
          return JsonResponse({'error': 'No valid language model found!'}, status=400)
        model_record = model_record[0]
        model_path = model_record.file
        if not model_path:
          return JsonResponse({'error': 'No language model found at specified path!'}, status=400)
        model_path = re.sub(r'\\{2,}', r'\\\\', model_path)
        model_path = os.path.join("E:", os.sep, 'VsCodeProjects', 'shaberu', 'files', 'system', 'models', 'gpt4all-falcon-q4_0.gguf')
        model_dir = os.path.dirname(model_path)
        model_file = os.path.basename(model_path)
        model = GPT4All(model_file, model_path=model_dir, allow_download=False, device='gpu')
        output = model.generate(input)
        data = {'result': output}
        return JsonResponse(data, status=200)


class ChatRowAjax(View):
    
    def post(self, request, *args, **kwargs):
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest': 
            return HttpResponseBadRequest()
        user_resp = request.POST.get('chat-user-resp')
        bot_resp = request.POST.get('chat-bot-resp')
        print(user_resp)
        print(bot_resp)

        # Get row partial
        partial_ctx = {'user_resp': user_resp, 'bot_resp': bot_resp}
        partial_url = "pages/partials/chat-response-row.html"
        partial_render = render_to_string(partial_url, partial_ctx)
        data = {'result': partial_render}
        print(data)
        return JsonResponse(data)
