# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import CodingProblem, TestCase

def problem_list_view(request):
    try:
        problems = CodingProblem.objects.all()[:100]
        return render(request, 'coding_problems/problems_list.html', {
            'problems': problems,
            'page_title': '100 Days Coding Challenge'
        })
    except Exception as e:
        return render(request, 'coding_problems/problems_list.html', {
            'error': f'Error loading problems: {str(e)}'
        })

def problem_detail_view(request, problem_id):
    try:
        problem = CodingProblem.objects.get(problem_id=problem_id)
        test_cases = TestCase.objects.filter(problem=problem)[:2]  # Using related_name='test_cases'
        return render(request, 'coding_problems/problems_detail.html', {
            'problem': problem,
            'test_cases': test_cases,
            'page_title': f'Problem {problem_id}: {problem.title}'
        })
    except CodingProblem.DoesNotExist:
        return render(request, 'coding_problems/problems_detail.html', {
            'error': 'Problem not found',
            'page_title': 'Problem Not Found'
        })
    except Exception as e:
        return render(request, 'coding_problems/problems_detail.html', {
            'error': f'Error loading problem: {str(e)}',
            'page_title': 'Error'
        })