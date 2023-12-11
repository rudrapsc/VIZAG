# streamapp/views.py
from django.shortcuts import render


    
def stream_view(request):
    return render(request, 'streamapp/video_stream.html')
