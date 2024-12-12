from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
import requests

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            login_data = {
                'email': email,
                'password': password
            }
            response = requests.post('http://localhost:8000/login/', json=login_data)
            
            if response.status_code == 200:
                # Parse response data
                data = response.json()
                user = data['user']
                
                # Lưu thông tin user vào session
                request.session['user_id'] = user['id']
                request.session['user_name'] = user['name']
                request.session['user_email'] = user['email']
                request.session['user_role'] = user['role']
                
                # Cập nhật tên user trong common.js
                return render(request, 'dashboard.html', {
                    'user_name': user['name']
                })
            else:
                return render(request, 'login.html', {
                    'error_message': 'Invalid email or password'
                })
                
        except requests.exceptions.RequestException:
            return render(request, 'login.html', {
                'error_message': 'Cannot connect to login service'
            })
    
    return render(request, 'login.html')

def register_view(request):
    template = loader.get_template('register.html')
    return HttpResponse(template.render())

def dashboard_view(request):
    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render())

def overall_view(request):
    template = loader.get_template('overall.html') 
    return HttpResponse(template.render())

def modelling_view(request):
    template = loader.get_template('modelling.html')
    return HttpResponse(template.render())

def predict(request):
    if request.method == 'POST':
        try:
            # Tách blood pressure thành systolic và diastolic
            bp = request.POST.get('bloodPressure', '').split('/')
            systolic = float(bp[0]) if len(bp) > 0 else 0
            diastolic = float(bp[1]) if len(bp) > 1 else 0

            # Chuyển đổi dữ liệu form sang format mà API mong đợi
            input_data = {
                'Gender': request.POST.get('gender'),
                'Height': float(request.POST.get('height')),
                'Weight': float(request.POST.get('weight')),
                'Cholesterol': float(request.POST.get('cholesterol')),
                'BMI': float(request.POST.get('bmi')),
                'Blood_Glucose': float(request.POST.get('bloodGlucose')),
                'Bone_Density': float(request.POST.get('boneDensity')),
                'Vision': float(request.POST.get('visionSharpness')),
                'Hearing': float(request.POST.get('hearingAbility')),
                'Physical_Activity': request.POST.get('physicalActivity'),
                'Smoking': request.POST.get('smokingStatus'),
                'Alcohol': request.POST.get('alcoholConsumption'),
                'Diet': request.POST.get('diet'),
                'Chronic_Diseases': request.POST.get('chronicDiseases'),
                'Medication': request.POST.get('medicationUse'),
                'Family_History': request.POST.get('familyHistory'),
                'Cognitive_Function': float(request.POST.get('cognitiveFunction')),
                'Mental_Health': request.POST.get('mentalHealthStatus'),
                'Sleep': request.POST.get('sleepPatterns'),
                'Stress': float(request.POST.get('stressLevels')),
                'Pollution': float(request.POST.get('pollutionExposure')),
                'Sun_Exposure': float(request.POST.get('sunExposure')),
                'Education': request.POST.get('educationLevel'),
                'Income': request.POST.get('incomeLevel'),
                'Systolic_BP': systolic,
                'Diastolic_BP': diastolic
            }

            # Đóng gói dữ liệu theo format API yêu cầu
            api_data = {
                'input_data': input_data
            }

            # Gọi API để lấy dự đoán
            response = requests.post('http://localhost:8000/api/predict/', json=api_data)
            
            if response.status_code == 200:
                prediction_data = response.json()
                predicted_age = prediction_data.get('predicted_age')
                
                return render(request, 'modelling.html', {
                    'prediction_result': predicted_age,
                    'form_data': request.POST  # Giữ lại dữ liệu form
                })
            else:
                error_message = response.json().get('error', 'Unknown error occurred')
                return render(request, 'modelling.html', {
                    'error_message': f'API Error: {error_message}',
                    'form_data': request.POST
                })
                
        except Exception as e:
            return render(request, 'modelling.html', {
                'error_message': f'Error processing form data: {str(e)}',
                'form_data': request.POST
            })
    
    return redirect('modelling')

def logout_view(request):
    # Clear session
    request.session.flush()
    return redirect('login')