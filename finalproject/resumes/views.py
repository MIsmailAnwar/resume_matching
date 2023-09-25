from django.shortcuts import render
from .forms import JobDescriptionForm
from processing import text_cleaning, calculate_similarity, calculate_similarity_word2vec
from django.http import HttpResponse
from django.conf import settings
import os

# Create your views here.

def match_candidates(request):
    if request.method == 'POST':
        form = JobDescriptionForm(request.POST)
        if form.is_valid():
            job_description = form.cleaned_data['job_description']
            job_description = text_cleaning(job_description)

            similarity_method = form.cleaned_data['similarity_method']  # Get the selected similarity method

            if similarity_method == 'tfidf':
                ranked_profiles = calculate_similarity(job_description)
            elif similarity_method == 'word2vec':
                ranked_profiles = calculate_similarity_word2vec(job_description)
            else:
                ranked_profiles = []  # Handle unsupported method (optional)

            return render(request, 'match_results.html', {'ranked_profiles': ranked_profiles})
    else:
        form = JobDescriptionForm()

    return render(request, 'match_form.html', {'form': form})



def serve_pdf_by_filename(request, filename):
    # Define the directory where your PDF files are stored.
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'pdf_files')  # Update with your directory path.

    # Construct the full file path based on the filename.
    #pdf_path = os.path.join(pdf_dir, filename)
    pdf_path = os.path.join(pdf_dir, f'{filename}.pdf')
    print(pdf_path)
    # Check if the file exists.
    if os.path.exists(pdf_path):
        # Open the PDF file and create a FileResponse object.
        with open(pdf_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{filename}"'
            return response
    else:
        # Handle the case where the PDF file doesn't exist.
        return HttpResponse('PDF file not found', status=404)




