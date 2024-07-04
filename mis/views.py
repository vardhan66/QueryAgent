from django.shortcuts import render
from mis.utils.llm import get_llm_response, get_function_prototypes
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

@csrf_exempt
def get_user_query(request):
    if request.method == "POST":
        system_prompt: str = \
        """
        You are a function call generator.
        Based on the provided function prototypes choose a function that is relevant 
        to the user's query, then extract required parameters from the user query
        and pass them to the function in the required format.
        Return the generated raw function call. Don't give any explanation.
        """

        
        responses: list[str] = []
        data = json.loads(request.body)
        print("This is data: ", data, type(data))
        
        prompt_category = json.loads(data['prompt_category'])
        function_prototypes: list[str] = get_function_prototypes(prompt_category)
            
        for prototype in function_prototypes: 
            full_user_prompt = f"""System:{system_prompt}\nFunctions:{prototype}\nUserQuery:{data['user_query']}"""
            response = get_llm_response("llama3", full_user_prompt)
            responses.append(response)

        return HttpResponse(''.join(responses))

