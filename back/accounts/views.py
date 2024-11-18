from django.shortcuts import render

def sample_view(request):
    return render(request, 'sample_template.html')