import os
import sys
import pandas as pd
import django

# Import Django settings and models
sys.path.append(os.path.realpath('..'))  # Add the project directory to the Python path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finalproject.settings')  # Set the Django settings module
django.setup()  # Initialize the Django environment

# Import the Resume model and text_cleaning
from resumes.models import Resume  
from processing import text_cleaning  

# Read the Excel file
excel_file = 'resume_final_data.xlsx'
df = pd.read_excel(excel_file, engine='openpyxl')

# Clear the database before insertion
Resume.objects.all().delete()

# Iterate through the DataFrame
for index, row in df.iterrows():
    # Apply text processing
    cleaned_resume_text = text_cleaning(row['Resume'])

    # Create and save a new Resume object in the database
    add = Resume.objects.create(filename=row['Filename'], title=row['Title'], resume_text=cleaned_resume_text)
    add.save()

# Print a completion message
print('DONE')


           