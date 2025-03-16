from django.shortcuts import get_object_or_404, render, redirect
from .models import UserRegistrations, UserStreak
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from yt_learning.models import save_watch_later
from django.contrib.auth.decorators import login_required

def Register_View(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # Validation: Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

        # Validation: Check if username is already taken
        if UserRegistrations.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'accounts/register.html')

        # Validation: Check if email is already taken
        if UserRegistrations.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return render(request, 'accounts/register.html')

        # Create the user if all validations pass
        try:
            # Use create_user() to securely hash the password
            user = UserRegistrations.objects.create(username=username, email=email, password=make_password(password),)
            user.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login')  # Redirect to login page after successful registration
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return render(request, 'accounts/register.html')

    # Render the registration form for GET requests
    return render(request, 'accounts/register.html')

def Login_View(request):
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        password = request.POST.get('password')

        #fetch user from database
        try: 
            user = UserRegistrations.objects.get(email=email)
        except UserRegistrations.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'accounts/login.html')
        
        #Validate password
        if not check_password(password, user.password):
            messages.error(request, 'Invalid email or password.')
            return render(request, 'accounts/login.html')
        
        # set user session
        request.session['user_id'] = user.id
        request.session['email']  = user.email
        request.session['username'] = user.username
        messages.success(request, 'Login successful.')
        return redirect('categories_page') 
    
    return render(request, 'accounts/login.html')

def Logout_View(request):
    request.session.flush()
    messages.success(request, 'Logout successful.')
    return redirect('login')






def Profile_View(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    user = get_object_or_404(UserRegistrations, id=user_id)
    
    # Get or create streak
    try:
        streak = UserStreak.objects.get(user=user)
    except UserStreak.DoesNotExist:
        streak = UserStreak.objects.create(user=user)
    
    # Update streak
    streak.update_streak()

    # Retrieve saved videos
    saved_videos = (
        save_watch_later.objects
        .filter(user=user)
        .select_related('video')
        .order_by('date')
    )
    
    context = {
        'user': user,
        'saved_videos': saved_videos,
        'current_streak': streak.streak_count,
        'longest_streak': streak.longest_streak,
        'last_visit': streak.last_visit,
    }
    return render(request, 'accounts/profile.html', context)


def Register_Category_View(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # Validation: Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

        # Validation: Check if username is already taken
        if UserRegistrations.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'accounts/register.html')

        # Validation: Check if email is already taken
        if UserRegistrations.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return render(request, 'accounts/register.html')

        # Create the user if all validations pass
        try:
            # Use create_user() to securely hash the password
            user = UserRegistrations.objects.create(username=username, email=email, password=make_password(password),)
            user.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login_category')  # Redirect to login page after successful registration
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return render(request, 'accounts/register.html')

    # Render the registration form for GET requests
    return render(request, 'accounts/register.html')


def Login_Category_View(request):
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        password = request.POST.get('password')

        #fetch user from database
        try: 
            user = UserRegistrations.objects.get(email=email)
        except UserRegistrations.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'accounts/login.html')
        
        #Validate password
        if not check_password(password, user.password):
            messages.error(request, 'Invalid email or password.')
            return render(request, 'accounts/login.html')
        
        # set user session
        request.session['user_id'] = user.id
        request.session['email']  = user.email
        request.session['username'] = user.username
        messages.success(request, 'Login successful.')
        #take category_id from the form and redirect to videos_by_category
        category_id=request.session.get('category_id')
        return redirect('videos_by_category', category_id=category_id)
    
    return render(request, 'accounts/login.html')