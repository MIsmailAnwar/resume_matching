from django import forms

class JobDescriptionForm(forms.Form):
    job_description = forms.CharField(
        label='Job Description',
        widget=forms.Textarea(attrs={'placeholder': 'Enter the job description here'}),
        required=True,
        max_length=5000,
    )

    similarity_method = forms.ChoiceField(
        label='Similarity Calculation Method',
        choices=[
            ('tfidf', 'TF-IDF'),
            ('word2vec', 'Word2Vec'),
        ],
        widget=forms.RadioSelect,
        initial='tfidf', 
    )
