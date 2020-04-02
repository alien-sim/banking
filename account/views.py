from django.shortcuts import render

# Create your views here.
def home(request):
	try:
		print("home")
		return render(request, 'index.html')
	except Exception as e:
		print("exception in home -- ", e)
		return render(request, 'index.html')