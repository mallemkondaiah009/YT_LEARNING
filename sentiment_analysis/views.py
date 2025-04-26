
import joblib
import os
from django.shortcuts import render
from django.http import JsonResponse

# Load the model
model_path = 'models/sentiment_model_78.pkl'
model = joblib.load(model_path)

def analyze_sentiment(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        if text:
            sentiment = model.predict([text])[0]
            sentiment_label = 'positive' if sentiment == 1 else 'negative'
            return JsonResponse({'sentiment': sentiment_label})
        else:
            return JsonResponse({'error': 'No text provided'}, status=400)
    return render(request, 'sentiment_analysis/sentiment_analizer.html')


