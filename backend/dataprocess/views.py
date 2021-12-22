from django.shortcuts import render

# Create your views here.


from django.shortcuts import render

# Create your views here.

def base(request):
    return render(request, 'dataprocess/main.html')
