import json
from django.db.models import Case, When, IntegerField
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string, get_template
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Choice, Question, PersonalCare, Category, QuizModal, Customer, Hydration, Concerns, Products
from .forms import CustomerForm
from .serializers import ChoiceSerializer, QuestionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q, F, Count, Sum
from .score import oil_dry_anls, sen_res_anls, acne_anls, pigmentation_anls, wrinkletight_anls, product_info

def index(request):
    """wellcome page"""
    context = {
        'form': CustomerForm()
    }
    return render(request, 'quizapp/index.html', context)


@csrf_exempt
def create_customer(request):
    """create_customer """
    data = dict()
    if request.method == "POST":
        emp_id = request.POST.get('employee_id')
        if Customer.objects.filter(employee_id=emp_id).exists():
            user_info = Customer.objects.get(employee_id=emp_id)
            data['exists'] = user_info.employee_id
            data['html_data'] = render_to_string('quizapp/customer_info.html',
            {'user_info': user_info}, request=request)
        else:
            form = CustomerForm(request.POST)
            if form.is_valid():
                fs = form.save()
                data['form_is_valid'] = True
                data['user_info'] = fs.employee_id
            else:
                data['form_is_valid'] = False
        return JsonResponse(data, safe=False)


def skin_quiz(request):
    primary = request.GET.get('primary')
    category_choice = request.GET.getlist('checkbox')
    user_name = request.GET.get('user_name')
    try:
        customer_obj = Customer.objects.get(employee_id=user_name)
    except ObjectDoesNotExist:
        customer_obj = None

    specific_concerns = [104, 105, 106]
            
    if category_choice and primary:
        category_data  = Category.objects.filter(pk__in=category_choice)
        concerns_save = Concerns()
        concerns_save.customer = customer_obj
        concerns_save.is_primary = Category.objects.get(pk=primary)
        concerns_save.save()
        for x in category_data:
            concerns_save.category.add(x)
        
        questions_data = Question.objects.filter(Q(category_id__in=category_choice) & ~Q(category__code__in=specific_concerns))
        if customer_obj.get_gender_display() == 'Male':
            questions_data = questions_data.filter(~Q(code=119)) #specific_concerns.append(119)

        if questions_data.exists():
            questions = questions_data.annotate(concern_sort=Case(When(category_id=primary, then=1), default=0, output_field=IntegerField()))
            questions.order_by('-concern_sort')
        else:
            return redirect('quizapp:products', user_name=customer_obj.employee_id)
    else:
        questions = Question.objects.filter(category__personalcare_id=1).order_by('code')
        #questions = Question.objects.filter(code__in=[107,108,109]).order_by('code')
    
    
    if primary:
        next_quiz = False
    else:
        next_quiz = True
    context = {
        'questions': questions,
        'next_quiz' : next_quiz,
        'primary' : primary
    }
    return render(request, 'quizapp/skin_quiz.html', context)


def skin_concerns(request, user_name):
    try:
        customer_id = Customer.objects.get(employee_id=user_name)
    except ObjectDoesNotExist:
        customer_id = None
    
    oil_dry_ctx = oil_dry_anls(customer_id)
    #print(oil_dry_ctx['oil_dry_analysis'])

    pc_data = get_object_or_404(PersonalCare, id=2)
    category = Category.objects.filter(personalcare_id=pc_data.id)
    context = {
        'category': category,
        'pc_data': pc_data,
        'oil_dry_ctx' : oil_dry_ctx
    }
    return render(request, 'quizapp/skin_concerns.html', context)


@csrf_exempt
def quiz_answers(request):
    data = dict()
    user_name = request.GET.get('user_name')
    user_choice = request.GET.get('user_choice')
    try:
        customer_obj = Customer.objects.get(employee_id=user_name)
    except ObjectDoesNotExist:
        customer_obj = None

    choice_data = json.loads(user_choice)

    if choice_data:
        for x in choice_data:
            try:
                choice_obj = Choice.objects.get(pk=x)
                quiz_save = QuizModal()
                quiz_save.choice = choice_obj
                quiz_save.customer = customer_obj
                quiz_save.save()
            except ObjectDoesNotExist:
                pass
                #choice_obj = get_object_or_404(Choice, pk=x) 
    data = {
        'saved': True
    }
    return JsonResponse(data, safe=False)


@csrf_exempt
def water_info(request):
    data = dict()
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        weight = request.POST.get('weight')
        physical_activity = request.POST.get('physical_activity')
        water_intake = request.POST.get('water_intake')
        status = request.POST.get('status')
        
        if Customer.objects.filter(employee_id=user_name).exists():
            customer_obj = Customer.objects.get(employee_id=user_name)
            water_save = Hydration()
            water_save.customer = customer_obj
            water_save.weight = weight
            water_save.physical_activity = physical_activity
            water_save.water_intake = water_intake
            water_save.status = status
            water_save.save()
            data['is_valid'] = True
        else:
           data['is_valid'] = False
    return JsonResponse(data, safe=False)

def products(request, user_name):
    """return products information as per username"""
    try:
        customer_id = Customer.objects.get(employee_id=user_name)
    except ObjectDoesNotExist:
        customer_id = None
    oil_dry_ctx = oil_dry_anls(customer_id)
    sen_res_ctx = sen_res_anls(customer_id)
    acne_anls_ctx = acne_anls(customer_id)
    ph_anls_ctx = QuizModal.objects.get(choice__question__code=108, customer=customer_id)

    pigmentation_anls_ctx = pigmentation_anls(customer_id)
    wrinkletight_anls_ctx = wrinkletight_anls(customer_id)
    concerns_data = Concerns.objects.get(customer=customer_id)
    product_data = product_info(customer_id, oil_dry_ctx, sen_res_ctx, acne_anls_ctx)

    context = {
        'oil_dry_ctx' : oil_dry_ctx,
        'sen_res_ctx' : sen_res_ctx,
        'acne_anls_ctx' : acne_anls_ctx,
        'pigmentation_anls_ctx' : pigmentation_anls_ctx,
        'wrinkletight_anls_ctx' : wrinkletight_anls_ctx,
        'ph_anls_ctx' : ph_anls_ctx,
        'concerns' : concerns_data,
        'pro_obj' : product_data
    }
    return render(request, 'quizapp/products.html', context)