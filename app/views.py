from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import HttpResponse
from io import BytesIO
from keras.models import load_model
from django.conf import settings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
import requests
from xhtml2pdf import pisa


# Loading my model
# Replace the GitHub URL with the actual URL to your model file
model_url = "https://github.com/JatinJaglan347/model-prediction-life-expectency-ultimate-accuracy-/raw/main/model%20prediction%20life%20expectency%20ultimate%20accuracy%20.h5"

# Download the model from the URL
response = requests.get(model_url)
model_content = BytesIO(response.content)

# Save the downloaded content to a temporary file
temp_file_path = "temp_model.h5"
with open(temp_file_path, "wb") as temp_file:
    temp_file.write(response.content)

# Load the model from the temporary file
model = load_model(temp_file_path)

# Optional: Remove the temporary file
import os
os.remove(temp_file_path)


def HomePage(request):
    print("I tried boss")
    if request.method == 'POST':
        print("I tried boss. Reached inside POST")
        name = request.POST.get('Name', '')
        gender =  request.POST.get('gender')
        age =  request.POST.get('Age')
        weight =  request.POST.get('Weight')
        height =  request.POST.get('Height')
        marital_status =  request.POST.get('MaritalStatus')
        annual_income =  request.POST.get('AnnualIncome')
        general_health =  request.POST.get('fitness')
        exercise =  int(request.POST.get("Exercise"))
        diabetic =  request.POST.get('diabetic')
        alcohol =  int(request.POST.get('Alcohol'))
        smoking =  request.POST.get('smoking')
        domestic_environment =  request.POST.get('DomesticEnvironment')
        medication_consumption =  request.POST.get('MedicineConsumption')
        nutrition =  request.POST.get('Nutrition')
        social_life =  request.POST.get('SocialLife')
        sleep_schedule =  request.POST.get('SleepSchedule')
        chronic_mental_health =  request.POST.get('ChronicMentalHealth')

        print(gender,age,weight,height,marital_status,annual_income,general_health,exercise,diabetic,alcohol,smoking,domestic_environment,medication_consumption,nutrition,social_life,sleep_schedule,chronic_mental_health)
        print("Marital Status",marital_status)

# Creating arrays for great, fair and poor performing areas
        great_performing_areas = []
        fair_performing_areas = []
        poor_performing_areas = []

        # Transforming the recieved data in a format that model can interpret
        user_input_array = []
        # Age / Current Age
        user_input_array.append(int(age))
       # Height
        user_input_array.append(int(height)) 
       # weight
        user_input_array.append(int(weight))   
        # Gender
        if(gender == "male"):
            user_input_array.append(1)
        else:
            user_input_array.append(0)  
        # Annual Income /Financial Situation  (Static for now)
        '''
        0: 1-3
        1: 3-5
        2: 5-8
        3: 8-15
        4: 15 above
        '''
        annual_income = int(annual_income)
        if(annual_income >= 1 and annual_income <=3):
            user_input_array.append(0)
        elif(annual_income >=3 and annual_income <= 5):
            user_input_array.append(1)
        elif(annual_income >=5 and annual_income <= 8):
            user_input_array.append(2)
        elif(annual_income >=8 and annual_income <= 15):
            user_input_array.append(3)
        elif(annual_income > 15):
            user_input_array.append(4)

       # Fitness / Workout  (Static for now)
        if(exercise == 0):
            user_input_array.append(0)
            poor_performing_areas.append("Exercise")
        elif(exercise == 1 or exercise == 2):
            user_input_array.append(1)
            fair_performing_areas.append("Exercise")
        elif(exercise == 3 or exercise == 4):
            user_input_array.append(2)
            great_performing_areas.append("Exercise")
        elif(exercise == 5 or exercise == 6):
            user_input_array.append(3)
            great_performing_areas.append("Exercise")
        elif(exercise == 7):
            user_input_array.append(4)
            great_performing_areas.append("Exercise")
        else:
            user_input_array.append(3)

        # General Health 
        if(general_health == "poor"):
            user_input_array.append(0)
            poor_performing_areas.append("General Health")
        elif(general_health == "fair"):
            user_input_array.append(1)
            fair_performing_areas.append("General Health")
        elif(general_health == "good"):
            user_input_array.append(2)
            great_performing_areas.append("General Health")
        elif(general_health == "VeryGood"):
            great_performing_areas.append("General Health")
            user_input_array.append(3)  
        elif(general_health == "excellent"):
            great_performing_areas.append("General Health")
            user_input_array.append(4)     
        else:
            user_input_array.append(3)
            
        #  Alcohol   (Static for now)
        if(alcohol <= 12 and alcohol >= 5):
            user_input_array.append(0)
            poor_performing_areas.append("Alcohol Consumption")
        elif(alcohol > 3 and alcohol < 5):
            user_input_array.append(1)
            poor_performing_areas.append("Alcohol Consumption")
        elif(alcohol >= 2 and alcohol <= 3):
            user_input_array.append(2)
            fair_performing_areas.append("Alcohol Consumption")
        elif(alcohol == 1):
            user_input_array.append(1)
            great_performing_areas.append("Alcohol Consumption")
        elif(alcohol == 0):
            user_input_array.append(0)
            great_performing_areas.append("Alcohol Consumption")


        # Smoking  (Static for now)
        if(smoking == "StillMoreThanOnePack"):
            user_input_array.append(0)
            poor_performing_areas.append("Smoking")
        elif(smoking == "StillOnePack"):
            user_input_array.append(1)
            poor_performing_areas.append("Smoking")
        elif(smoking == "StillHalfPackOrLess"):
            user_input_array.append(2)
            poor_performing_areas.append("Smoking")
        elif(smoking == "QuitGreaterThan10YearAgo"):
            user_input_array.append(5)
            great_performing_areas.append("Smoking")
        elif(smoking == "quit_one_two_nine_year_ago"):
            user_input_array.append(4)     
            great_performing_areas.append("Smoking")
        elif(smoking == "quit_less_than_one_year_ago"):
            user_input_array.append(3)        
            great_performing_areas.append("Smoking")
        elif(smoking == "never"):
            user_input_array.append(6)           
            great_performing_areas.append("Smoking")
         

        # Marital Status

        # Married, never married, divorced
        if(marital_status == "married"):
            user_input_array.append(1)
            user_input_array.append(0)
            user_input_array.append(0)

        elif(marital_status == "not_married"):
            user_input_array.append(0)
            user_input_array.append(1)
            user_input_array.append(0)
        elif(marital_status == "divorced"):
            user_input_array.append(0)
            user_input_array.append(0)
            user_input_array.append(1) 
        elif(marital_status == "prefer_not_to_say"):
            user_input_array.append(0)
            user_input_array.append(0)
            user_input_array.append(0)  
        else:
            user_input_array.append(0)
            user_input_array.append(0)
            user_input_array.append(0)             

        # Diabetic
        if(diabetic == "Yes"):
            user_input_array.append(0)
        else:
            user_input_array.append(1)

        # Nutrition
        if(nutrition == "JunkFoodAddict"):
            user_input_array.append(0)
            poor_performing_areas.append("Nutrition")
        elif(nutrition == "HealthyForTheMostPart"):
            user_input_array.append(1)
            great_performing_areas.append("Nutrition")
        elif(nutrition == "OnlyOnSelectedDates"):
            user_input_array.append(2)
            great_performing_areas.append("Nutrition")
        elif(nutrition == "NoJunkFood"):
            user_input_array.append(3)
            great_performing_areas.append("Nutrition")
        else:
            user_input_array.append(3)


        # Social Life
        if(social_life == "None"):
                user_input_array.append(0)
                poor_performing_areas.append("Social Life")
        elif(social_life == "Barely"):
            user_input_array.append(1)
            poor_performing_areas.append("Social Life")
        elif(social_life == "Healthy"):
            user_input_array.append(2) 
            great_performing_areas.append("Social Life")
        elif(social_life == "ManyCloseFriends"):
            user_input_array.append(3)
            great_performing_areas.append("Social Life")
        else:
            user_input_array.append(3)

        #chronic_mental_health
        if(chronic_mental_health == "Depressed-Pessimistic"):
                user_input_array.append(0)
                poor_performing_areas.append("Mental Health")
        elif(chronic_mental_health == "Stressed-Worried"):
            user_input_array.append(1)
            poor_performing_areas.append("Mental Health")
        elif(chronic_mental_health == "Complex"):
            user_input_array.append(2) 
            fair_performing_areas.append("Mental Health")
        elif(chronic_mental_health == "Positive"):
            user_input_array.append(3)  
            great_performing_areas.append("Mental Health")
        elif(chronic_mental_health == "Calm"):
            user_input_array.append(4)           
            great_performing_areas.append("Mental Health")
        else:
            user_input_array.append(4)

       #Domestic Environment
        if(domestic_environment == "QuiteToxic"):
                user_input_array.append(0)
                poor_performing_areas.append("Domestic Environment")
        elif(domestic_environment == "PreferNotToSayDomesticEnvironment"):
            user_input_array.append(1)
        elif(domestic_environment == "HealthyVibes"):
            user_input_array.append(2) 
            poor_performing_areas.append("Domestic Environment")    
        elif(domestic_environment == "Peaceful"):
            poor_performing_areas.append("Domestic Environment")
            user_input_array.append(3)    
        elif(domestic_environment == "Uplifting"):
            great_performing_areas.append("Domestic Environment")
            user_input_array.append(4)   
        else:
            user_input_array.append(4)
            

        # Sleep Schedule (not actually using to predict)   
        print("Great Performing areas: ",great_performing_areas)
        print("fair Performing areas: ",fair_performing_areas) 
        print("poor Performing areas: ",poor_performing_areas)
        print("gener: ", gender)
        context = {
            
            'great_performing_areas': great_performing_areas,
            'fair_performing_areas': fair_performing_areas, 
            'poor_performing_areas': poor_performing_areas
            }
        
        User_details = {
            'Name': name,
            'gender': request.POST.get('gender', ''),
            'Age': age,
            'Weight': weight,
            'Height': height,
            'MaritalStatus': marital_status,
            'AnnualIncome': annual_income,
            'fitness': request.POST.get('fitness', ''),
            'Exercise': exercise,
            'diabetic': request.POST.get('diabetic', ''),
            'Alcohol': alcohol,
            'smoking': request.POST.get('smoking', ''),
            'DomesticEnvironment': domestic_environment,
            'MedicineConsumption': medication_consumption,
            'Nutrition': nutrition,
            'SocialLife': social_life,
            'SleepSchedule': sleep_schedule,
            'ChronicMentalHealth': chronic_mental_health,
        }
        
        # User_details={
        #     'user_inputs': user_inputs,
        # }

        print("Here is the final array -> ", user_input_array)
        prediction = model.predict([user_input_array])
        print(prediction)
        

        form_data = {
            'Name': request.POST.get('Name', ''), 
            'dob': request.POST.get('dob', ''),  
            'gender': request.POST.get('gender', ''),
            'Age': request.POST.get('Age', ''),
            'Weight': request.POST.get('Weight', ''),
            'Height': request.POST.get('Height', ''),
            'AnnualIncome': request.POST.get('AnnualIncome', ''),
            'MaritalStatus': request.POST.get('MaritalStatus', ''),
            'fitness': request.POST.get('fitness', ''),
            'Exercise': request.POST.get('Exercise', ''),
            'diabetic': request.POST.get('diabetic', ''),
            'Alcohol': request.POST.get('Alcohol', ''),
            'smoking': request.POST.get('smoking', ''),
            'DomesticEnvironment': request.POST.get('DomesticEnvironment', ''),
            'MedicineConsumption': request.POST.get('MedicineConsumption', ''),
            'Nutrition': request.POST.get('Nutrition', ''),
            'SocialLife': request.POST.get('SocialLife', ''),
            'SleepSchedule': request.POST.get('SleepSchedule', ''),
            'ChronicMentalHealth': request.POST.get('ChronicMentalHealth', ''),
            'prediction': round(prediction[0][0]),
            'prediction_max': round(prediction[0][0] + 4)
        }
        User_details = {
            'Name': name,
            'gender': request.POST.get('gender', ''),
            'Age': age,
            'Weight': weight,
            'Height': height,
            'MaritalStatus': marital_status,
            'AnnualIncome': annual_income,
            'fitness': request.POST.get('fitness', ''),
            'Exercise': exercise,
            'diabetic': request.POST.get('diabetic', ''),
            'Alcohol': alcohol,
            'smoking': request.POST.get('smoking', ''),
            'DomesticEnvironment': domestic_environment,
            'MedicineConsumption': medication_consumption,
            'Nutrition': nutrition,
            'SocialLife': social_life,
           'SleepSchedule': sleep_schedule,
            'ChronicMentalHealth': chronic_mental_health,
        }


        
        
        
        # Google Apps Script URL
        script_url = 'https://script.google.com/macros/s/AKfycbyDwR8oUj9m0qSGfW4MwYc7p4Eak9MZkjzLCltEKbg_vh1b3mq8iNYnAcl-i3Ech8-Ofw/exec'

        # Send a POST request to the Google Apps Script URL
        response = requests.post(script_url, data=form_data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Form submitted successfully to Google Sheets")
        else:
            print("Error submitting form to Google Sheets")
    

        return render(request,"output_page.html", {'prediction': round(prediction[0][0]),'prediction_max': round(prediction[0][0] + 4),"Performance":context , "Details":User_details,})
    
    return render(request,"home.html")
    

def OutputPage(request):
    return render(request,"output_page.html")


