from django.db.models import Q, F, Count, Sum
from django.core.exceptions import ObjectDoesNotExist
from quizapp.models import (Choice, Question, PersonalCare, Category, QuizModal,
Customer, Hydration, Concerns, Products)


STATEMENT  = [
    ("1", "Oily Skin"),
    ("2", "Combination Skin (Slightly Oily)"),
    ("3", "Normal Skin"),
    ("4", "Dry Skin")
]


def quality(q):
    for k, v in STATEMENT:
        if v == q:
            return q


def oil_dry_anls(customer_id):
    skin = QuizModal.objects.filter(Q(choice__question__category__code=100) & Q(customer=customer_id))
    #CustomUser.objects.filter(username__in=created_by).values_list('email', flat=True)
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
    
    final_output = ''
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

    try:
        hydration = Hydration.objects.get(customer_id=customer_id)
    except ObjectDoesNotExist:
        hydration = None
    context = {
        'skin':skin,
        'strip_score': strip_score,
        'strip_analysis' : strip_analysis,
        'quiz_score': quiz_score,
        'quiz_analysis' : quiz_analysis,
        'oil_dry_analysis' : final_output,
        'hydration' : hydration.status
    }
    return context


SEN_RES_STATEMENT  = [
    ("1", "Sensitive Skin"),
    ("2", "Somewhat Sensitive Skin"),
    ("3", "Somewhat Resistant Skin"),
    ("4", "Resistant Skin")
]

def sen_res_anls(customer_id):
    skin = QuizModal.objects.filter(Q(choice__question__category__code=102) & Q(customer=customer_id))
    sen_res_score = skin.aggregate(Sum('choice__marks'))['choice__marks__sum'] or 0.00
    sen_res_analysis = ''
    if sen_res_score:
        if 11 <= sen_res_score <= 20:
            sen_res_analysis = SEN_RES_STATEMENT[0][1]
        elif 9 <= sen_res_score <= 10:
            sen_res_analysis = SEN_RES_STATEMENT[1][1]
        elif 7 <= sen_res_score <= 8:
            sen_res_analysis = SEN_RES_STATEMENT[2][1]
        elif 5 <= sen_res_score <= 6:
            sen_res_analysis = SEN_RES_STATEMENT[3][1]
    
    context = {
        'sen_res_score': sen_res_score,
        'sen_res_analysis' : sen_res_analysis,
    }
    return context


ACNE_STATEMENT  = [
    ("1", "Mild Acne"),
    ("2", "Moderate Acne"),
    ("3", "Severe Acne")
]

def acne_anls(customer_id):
    skin = QuizModal.objects.filter(Q(choice__question__category__code=103) & Q(customer=customer_id))
    acne_score = skin.aggregate(Sum('choice__marks'))['choice__marks__sum'] or 0.00
    acne_analysis = ''
    if acne_score:
        if 5 <= acne_score <= 8:
            acne_analysis = ACNE_STATEMENT[0][1]
        elif 9 <= acne_score <= 12:
            acne_analysis = ACNE_STATEMENT[1][1]
        elif 13 <= acne_score <= 20:
            acne_analysis = ACNE_STATEMENT[2][1]
    
    context = {
        'acne_score': acne_score,
        'acne_analysis' : acne_analysis
    }
    return context


PIGMENTATION_STATEMENT = [
    ("1", "Severe Hyperpigmentation"),
    ("2", "Moderate Hyperpigmented"),
    ("3", "No Hyperpigmentation")
]

def pigmentation_anls(customer_id):
    skin = QuizModal.objects.filter(Q(choice__question__category__code=107) & Q(customer=customer_id))
    pigmentation_score = skin.aggregate(Sum('choice__marks'))['choice__marks__sum'] or 0.00
    pigmentation_analysis = ''
    if pigmentation_score:
        if 12 <= pigmentation_score <= 20:
            pigmentation_analysis = PIGMENTATION_STATEMENT[0][1]
        elif 9 <= pigmentation_score <= 11:
            pigmentation_analysis = PIGMENTATION_STATEMENT[1][1]
        elif 5 <= pigmentation_score <= 8:
            pigmentation_analysis = PIGMENTATION_STATEMENT[2][1]
    
    context = {
        'pigmentation_score': pigmentation_score,
        'pigmentation_analysis' : pigmentation_analysis
    }
    return context

WRINKLETIGHT_STATEMENT = [
    ("1", "Mild signs of Aging"),
    ("2", "Moderate signs of Ageing"),
    ("3", "Severe signs of Ageining")
]

def wrinkletight_anls(customer_id):
    skin = QuizModal.objects.filter(Q(choice__question__category__code=108) & Q(customer=customer_id))
    wrinkletight_score = skin.aggregate(Sum('choice__marks'))['choice__marks__sum'] or 0.00
    wrinkletight_analysis = ''
    if wrinkletight_score:
        if 6 <= wrinkletight_score <= 9:
            wrinkletight_analysis = WRINKLETIGHT_STATEMENT[0][1]
        elif 10 <= wrinkletight_score <= 14:
            wrinkletight_analysis = WRINKLETIGHT_STATEMENT[1][1]
        elif 15 <= wrinkletight_score <= 24:
            wrinkletight_analysis = WRINKLETIGHT_STATEMENT[2][1]
    
    context = {
        'wrinkletight_score': wrinkletight_score,
        'wrinkletight_analysis' : wrinkletight_analysis
    }
    return context

def product_info(customer_id, oil_dry_ctx, sen_res_ctx, acne_anls_ctx):
    try:
        concern_obj = Concerns.objects.get(customer=customer_id)
    except ObjectDoesNotExist:
        concern_obj = None
    
    #print(sen_res_ctx['sen_res_analysis'])
    #print(oil_dry_ctx['oil_dry_analysis'])
    #print(concern_obj.filter(is_primary__name='Oily Skin').values())
    #print(Concerns.objects.get(is_primary__name='Oily Skin'))
    #print(concern_obj.is_primary.name=='Oily Skin')

    pro_code = 0    
    if concern_obj.is_primary.name == 'Oily Skin':
        if oil_dry_ctx['oil_dry_analysis'] == 'Combination Skin (Slightly Oily)':
            pro_code = 103
        elif oil_dry_ctx['oil_dry_analysis'] == 'Oily Skin':
            pro_code = 104
    elif concern_obj.is_primary.name == 'Dry Skin':
        if oil_dry_ctx['oil_dry_analysis'] == 'Normal Skin':
            pro_code = 102
        elif oil_dry_ctx['oil_dry_analysis'] == 'Dry Skin':
            pro_code = 101
    elif concern_obj.is_primary.name == 'Sensitive Skin':
        if sen_res_ctx['sen_res_analysis'] == 'Sensitive Skin':
            pro_code = 105
    elif concern_obj.is_primary.name == 'Hyperpigmentation':
        if oil_dry_ctx['oil_dry_analysis'] == 'Dry Skin':
            pro_code = 106
        elif oil_dry_ctx['oil_dry_analysis'] == 'Normal Skin':
            pro_code = 107
        elif oil_dry_ctx['oil_dry_analysis'] == 'Combination Skin (Slightly Oily)':
            pro_code = 108
        elif oil_dry_ctx['oil_dry_analysis'] == 'Oily Skin':
            pro_code = 109
        elif sen_res_ctx['sen_res_analysis'] == 'Sensitive Skin':
            pro_code = 110
    elif concern_obj.is_primary.name == 'Antiagning':
        if oil_dry_ctx['oil_dry_analysis'] == 'Dry Skin':
            pro_code = 111
        elif oil_dry_ctx['oil_dry_analysis'] == 'Normal Skin':
            pro_code = 112
        elif oil_dry_ctx['oil_dry_analysis'] == 'Combination Skin (Slightly Oily)':
            pro_code = 113
        elif oil_dry_ctx['oil_dry_analysis'] == 'Oily Skin':
            pro_code = 114
        elif sen_res_ctx['sen_res_analysis'] == 'Sensitive Skin':
            pro_code = 115
    elif concern_obj.is_primary.name == 'Acne':
        if acne_anls_ctx['acne_analysis'] == 'Mild Acne':
            if oil_dry_ctx['oil_dry_analysis'] == 'Dry Skin':
                pro_code = 121
            elif oil_dry_ctx['oil_dry_analysis'] == 'Normal Skin':
                pro_code = 122
            elif oil_dry_ctx['oil_dry_analysis'] == 'Combination Skin (Slightly Oily)':
                pro_code = 123
            elif oil_dry_ctx['oil_dry_analysis'] == 'Oily Skin':
                pro_code = 124
            elif oil_dry_ctx['oil_dry_analysis'] == 'Sensitive Skin':
                pro_code = 125
        elif acne_anls_ctx['acne_analysis'] == 'Moderate Acne':
            if oil_dry_ctx['oil_dry_analysis'] == 'Dry Skin':
                pro_code = 131
            elif oil_dry_ctx['oil_dry_analysis'] == 'Normal Skin':
                pro_code = 132
            elif oil_dry_ctx['oil_dry_analysis'] == 'Combination Skin (Slightly Oily)':
                pro_code = 133
            elif oil_dry_ctx['oil_dry_analysis'] == 'Oily Skin':
                pro_code = 134
            elif oil_dry_ctx['oil_dry_analysis'] == 'Sensitive Skin':
                pro_code = 135
        elif acne_anls_ctx['acne_analysis'] == 'Severe Acne':
            if oil_dry_ctx['oil_dry_analysis'] == 'Dry Skin':
                pro_code = 141
            elif oil_dry_ctx['oil_dry_analysis'] == 'Normal Skin':
                pro_code = 142
            elif oil_dry_ctx['oil_dry_analysis'] == 'Combination Skin (Slightly Oily)':
                pro_code = 143
            elif oil_dry_ctx['oil_dry_analysis'] == 'Oily Skin':
                pro_code = 144
            elif oil_dry_ctx['oil_dry_analysis'] == 'Sensitive Skin':
                pro_code = 145

    try:
        pro_obj = Products.objects.get(code=pro_code)
    except ObjectDoesNotExist:
        pro_obj = None
    
    return pro_obj