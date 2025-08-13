from django.shortcuts import render

def map_view(request):
    return render(request, 'map.html')
    
def our_view(request):
    return render(request, 'our.html')
    