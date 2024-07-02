from django.shortcuts import render
from mis.utils.llm import get_llm_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def get_prompt_category(request):
    full_user_prompt = \
    """
    Read the user query and classify the prompt into primary and secondary categories.
    Return the classified headings as dictionary where primary_category, secondary_category are keys
    and the actual categories as values. Don't give any explanation and only give raw data.
    If the query is categorized into more than one category then return values as a list.
    If no matching category is found return an empty list.

    Categories:
        GeneralQuery:
            StudentQueries:
                -- Get a list of student's details
                -- Get a specific student details
                -- Get a student's nptel_status
                -- Get a student's branch
                -- Get a student's mobile number
                -- Get a student's section

            FacultiesQueries:
                -- Get a list of all faculties
                -- Get a specific faculty details
                -- Get a faculty's phone number
   UserPrompt:
        {user_prompt}
    """

    if request.method == "POST":
        data = json.loads(request.body) 
        full_user_prompt = full_user_prompt.format(user_prompt=data['prompt'])
        response = get_llm_response('llama3', full_user_prompt)         
        return HttpResponse(response)

