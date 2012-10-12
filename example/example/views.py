from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

def homepage(request):

	if request.method == 'POST':
		form = AuthenticationForm(request=request, data=request.POST)		
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('home')
	else:
		form = AuthenticationForm(request=request)

	request.session.set_test_cookie()
	context = {
		'form': form
	}

	return render(request, 'home.html', context)