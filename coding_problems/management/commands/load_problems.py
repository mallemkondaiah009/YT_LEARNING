import json
from django.core.management.base import BaseCommand
from coding_problems.models import CodingProblem, TestCase

class Command(BaseCommand):
    help = 'Loads coding problems from a JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('coding.json', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        json_file = options['coding.json']

        try:
            with open(json_file, 'r') as file:
                data = json.load(file)

            created_problems = 0
            created_test_cases = 0

            for problem_data in data:
                # Create or update the CodingProblem
                problem, created = CodingProblem.objects.update_or_create(
                    problem_id=problem_data['id'],
                    defaults={
                        'title': problem_data['title'],
                        'problem': problem_data['problem'],
                        'input_desc': problem_data['input'],
                        'output_desc': problem_data['output'],
                    }
                )
                if created:
                    created_problems += 1

                # Clear existing test cases if updating
                if not created:
                    problem.test_cases.all().delete()

                # Add test cases
                for test_case_data in problem_data['test_cases']:
                    TestCase.objects.create(
                        problem=problem,
                        input_data=test_case_data['input'],
                        output_data=test_case_data['output']
                    )
                    created_test_cases += 1

            self.stdout.write(self.style.SUCCESS(
                f'Successfully loaded {created_problems} problems and {created_test_cases} test cases from {json_file}'
            ))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File {json_file} not found'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f'Invalid JSON format in {json_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))