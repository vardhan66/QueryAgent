from django.urls import path
from . import views

app_name = 'mis'

urlpatterns = [
        path('', views.get_prompt_category, name='promptcategory'),
        path('get_user_query/', views.get_user_query)
]

