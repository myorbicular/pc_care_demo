from django.db.models import Q, F, Count, Sum
from django.core.exceptions import ObjectDoesNotExist
from quizapp.models import Choice, Question, PersonalCare, Category, QuizModal, Customer, Hydration


STATEMENT  = [
    ("1", "Oily Skin"),
    ("2", "Combination Skin (Slightly Oily)"),
    ("3", "Normal Skin"),
    ("4", "Dry Skin")
]


def oil_dry_anls(customer_id):
    skin = QuizModal.objects.filter(Q(choice__question__category__code=100) & Q(customer=customer_id))
    strip_score = skin.filter(choice__question__code__in=[100,101]).aggregate(Sum('choice__marks'))['choice__marks__sum'] or 0.00
    strip_analysis = ''
    if strip_score:
        if 7 <= strip_score <= 8:
            strip_analysis = STATEMENT[0][1]
        elif 5 <= strip_score <= 6:
            strip_analysis = STATEMENT[1][1]
        elif 3 <= strip_score <= 4:
            strip_analysis = STATEMENT[2][1]
        elif 1 <= strip_score <= 2:
            strip_analysis = STATEMENT[3][1]
    
    quiz_score = skin.filter(~Q(choice__question__code__in=[100,101])).aggregate(Sum('choice__marks'))['choice__marks__sum'] or 0.00
    quiz_analysis = ''
    if quiz_score:
        if 16 <= quiz_score <= 20:
            quiz_analysis = STATEMENT[0][1]
        elif 12 <= quiz_score <= 15:
            quiz_analysis = STATEMENT[1][1]
        elif 8 <= quiz_score <= 11:
            quiz_analysis = STATEMENT[2][1]
        elif 5 <= quiz_score <= 7:
            quiz_analysis = STATEMENT[3][1]

    if strip_analysis == quiz_analysis:
        final_output = strip_analysis
    #Oily Skin
    elif strip_analysis == STATEMENT[0][1] and quiz_analysis == STATEMENT[1][1]:
        final_output = STATEMENT[0][1] #Oily Skin
    elif strip_analysis == STATEMENT[0][1] and quiz_analysis == STATEMENT[2][1]:
        final_output = STATEMENT[2][1] #Normal Skin
    elif strip_analysis == STATEMENT[0][1] and quiz_analysis == STATEMENT[3][1]:
        final_output = STATEMENT[3][1]
    
    #Combination Skin
    elif strip_analysis == STATEMENT[1][1] and quiz_analysis == STATEMENT[0][1]:
        final_output = STATEMENT[1][1] #Combination Skin
    elif strip_analysis == STATEMENT[1][1] and quiz_analysis == STATEMENT[2][1]:
        final_output = STATEMENT[1][1] #Combination Skin
    elif strip_analysis == STATEMENT[1][1] and quiz_analysis == STATEMENT[3][1]:
        final_output = STATEMENT[3][1] #Dry Skin
    
     #Normal Skin
    elif strip_analysis == STATEMENT[2][1] and quiz_analysis == STATEMENT[0][1]:
        final_output = STATEMENT[2][1] #Normal Skin
    elif strip_analysis == STATEMENT[2][1] and quiz_analysis == STATEMENT[1][1]:
        final_output = STATEMENT[1][1] #Combination Skin
    elif strip_analysis == STATEMENT[2][1] and quiz_analysis == STATEMENT[3][1]:
        final_output = STATEMENT[2][1] #Normal Skin
    
    #Dry Skin
    elif strip_analysis == STATEMENT[3][1] and quiz_analysis == STATEMENT[0][1]:
        final_output = STATEMENT[3][1] #Dry Skin
    elif strip_analysis == STATEMENT[3][1] and quiz_analysis == STATEMENT[1][1]:
        final_output = STATEMENT[3][1] #Dry Skin
    elif strip_analysis == STATEMENT[3][1] and quiz_analysis == STATEMENT[3][1]:
        final_output = STATEMENT[2][1] #Normal Skin

    context = {
        'strip_score': strip_score,
        'strip_analysis' : strip_analysis,
        'quiz_score': quiz_score,
        'quiz_analysis' : quiz_analysis,
        'oil_dry_analysis' : final_output,
    }
    return context