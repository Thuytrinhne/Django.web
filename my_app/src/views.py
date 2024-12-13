from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
import requests
import json

def home_view(request):
    # Kiểm tra xem user đã đăng nhập chưa
    if 'user_id' in request.session:
        return render(request, 'overall.html')
    else:
        return redirect('login')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            login_data = {
                'email': email,
                'password': password
            }
            response = requests.post('http://localhost:3000/login/', json=login_data)
            
            if response.status_code == 200:
                # Parse response data
                data = response.json()
                user = data['user']
                
                # Lưu thông tin user vào session
                request.session['user_id'] = user['id']
                request.session['user_name'] = user['name']
                request.session['user_email'] = user['email']
                request.session['user_role'] = user['role']
                
                # Chuyển hướng sang trang overall
                return redirect('home')
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
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Validate input
            if not all([name, email, password]):
                return render(request, 'register.html', {
                    'error_message': 'All fields are required'
                })
            
            # Call register API
            response = requests.post('http://localhost:3000/register/', json={
                'name': name,
                'email': email,
                'password': password
            })
            
            if response.status_code == 200:
                # Parse successful response
                data = response.json()
                user = data.get('user', {})
                
                # Store user info in session
                request.session['user_id'] = user.get('id')
                request.session['user_name'] = user.get('name') 
                request.session['user_email'] = user.get('email')
                
                # Render trang với thông báo thành công trước khi redirect
                return render(request, 'register.html', {
                    'success_message': 'User registered successfully',
                    'redirect_url': reverse('home')
                })
            else:
                # Handle error response
                error_data = response.json()
                error_message = error_data.get('message', 'Registration failed')
                return render(request, 'register.html', {
                    'error_message': error_message
                })
                
        except Exception as e:
            return render(request, 'register.html', {
                'error_message': str(e)
            })
    
    return render(request, 'register.html')

def dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    return render(request, 'dashboard.html')

def overall_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    return render(request, 'overall.html')

def modelling_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        try:
            # Xử lý form data và gọi API predict
            bp = request.POST.get('bloodPressure', '').split('/')
            systolic = float(bp[0].strip()) if len(bp) > 0 else 0
            diastolic = float(bp[1].strip()) if len(bp) > 1 else 0

            request_data = {
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
                'Chronic_Diseases': request.POST.get('chronicDiseases') or 'None',
                'Medication': request.POST.get('medicationUse') or 'No',
                'Family_History': request.POST.get('familyHistory') or 'None',
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

            response = requests.post('http://localhost:3000/predict/', json=request_data)
            
            if response.status_code == 200:
                response_data = response.json()
                return render(request, 'modelling.html', {
                    'prediction_result': round(response_data.get('prediction'), 2),
                    'prediction_message': response_data.get('message'),
                    'form_data': request.POST
                })
            else:
                error_message = response.json().get('error', 'Unknown error occurred')
                return render(request, 'modelling.html', {
                    'error_message': f'API Error: {error_message}',
                    'form_data': request.POST
                })

        except requests.exceptions.RequestException:
            return render(request, 'modelling.html', {
                'error_message': 'Cannot connect to prediction service',
                'form_data': request.POST
            })

    return render(request, 'modelling.html')

@csrf_protect
def predict(request):
    if request.method == 'POST':
        try:
            # Tách blood pressure thành systolic và diastolic
            bp = request.POST.get('bloodPressure', '').split('/')
            systolic = float(bp[0].strip()) if len(bp) > 0 else 0
            diastolic = float(bp[1].strip()) if len(bp) > 1 else 0

            # Chuyển đổi dữ liệu form sang format API
            request_data = {
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
                'Chronic_Diseases': request.POST.get('chronicDiseases') or 'None',
                'Medication': request.POST.get('medicationUse') or 'No',
                'Family_History': request.POST.get('familyHistory') or 'None',
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

            response = requests.post('http://localhost:3000/predict/', json=request_data)
            
            if response.status_code == 200:
                response_data = response.json()
                return render(request, 'modelling.html', {
                    'prediction_result': round(response_data.get('prediction'), 2),
                    'prediction_message': response_data.get('message'),
                    'form_data': request.POST
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
    
    return render(request, 'modelling.html')

def logout_view(request):
    # Clear session
    request.session.flush()
    return redirect('login')