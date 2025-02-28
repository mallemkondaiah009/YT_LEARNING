from django.shortcuts import render, get_object_or_404
from .models import Category, Videos, Bashalu
from accounts.models import UserRegistrations
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Videos, Category, save_watch_later

# Landing page view
def landing_page(request):
    return render(request, 'yt_learning/landing_page.html')

# Categories page view
def categories_page(request):
    categories = Category.objects.all()  # Fetch all categories from the database
    return render(request, 'yt_learning/category.html', {'categories': categories})


def videos_by_category(request, category_id):
    # Retrieve category
    category = get_object_or_404(Category, id=category_id)
    languages = Bashalu.objects.all()
    
    # Get selected language name from POST request or session
    selected_language_name = request.POST.get('language')
    if selected_language_name is not None:  # Explicitly check for None to allow empty string
        request.session['selected_language_name'] = selected_language_name
    else:
        selected_language_name = request.session.get('selected_language_name')
    
    # Retrieve videos for the category
    videos = Videos.objects.filter(category=category)
    print(f"Initial videos count: {videos.count()}")  # Debug: Total videos in category
    
    # Filter videos by selected language name if provided
    if selected_language_name:
        try:
            # Assuming 'bhashalu' is a ForeignKey to Bashalu, get the Bashalu object by lang_name
            language_obj = Bashalu.objects.get(lang_name=selected_language_name)
            videos = videos.filter(bhashalu=language_obj)
            print(f"Filtered videos count for {selected_language_name}: {videos.count()}")  # Debug: After language filter
        except Bashalu.DoesNotExist:
            videos = Videos.objects.none()
            print("Language name not found, returning empty queryset")
    
    # Retrieve saved video IDs using session
    saved_video_ids = []
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = UserRegistrations.objects.get(id=user_id)
            saved_video_ids = save_watch_later.objects.filter(user=user).values_list('video_id', flat=True)
        except UserRegistrations.DoesNotExist:
            saved_video_ids = []
    
    # Handle POST request for saving a video or changing language
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)
        
        action = request.POST.get('action')
        
        if action == 'save':
            video_id = request.POST.get('video_id')
            video = get_object_or_404(Videos, id=video_id)
            user = UserRegistrations.objects.get(id=user_id)
            if not save_watch_later.objects.filter(video=video, user=user).exists():
                save_watch_later.objects.create(video=video, user=user)
                return JsonResponse({'status': 'success', 'message': 'Video saved for later'})
            else:
                return JsonResponse({'status': 'info', 'message': 'Video already saved'})
        
        elif action == 'language':
            return JsonResponse({'status': 'success', 'message': 'Language changed'})
    
    # Render the page for GET requests
    print(f"Final videos count: {videos.count()}")  # Debug: Final count before rendering
    context = {
        'category': category,
        'languages': languages,
        'videos': videos,
        'saved_video_ids': list(saved_video_ids),
        'selected_language': selected_language_name,  # Pass selected language name to template
    }
    return render(request, 'yt_learning/videos_by_category.html', context)