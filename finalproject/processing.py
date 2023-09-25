from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import contractions
from resumes.models import Resume
from resumes.apps import ResumesConfig
import gensim
import numpy as np

translator = str.maketrans('', '', string.punctuation)
nlp = ResumesConfig.nlp

def text_cleaning(text):
    text = text.lower()
    text = text.translate(translator)
    text = " ".join(text.split())
    text = contractions.fix(text)
    return text
                                                                                                                                                                      
def calculate_similarity(job_description):
    # Preprocess job description
    job_description_p = nlp(job_description)

    # Get all resumes
    resumes = Resume.objects.all()

    # Preprocess resumes and extract keywords
    resume_keywords = []
    for resume in resumes:
        resume_text = resume.resume_text
        resume_p = nlp(resume_text)
        keywords = [token.text for token in resume_p]
        resume_keywords.append(keywords)

    # TF-IDF Vectorization
    tfidf_vectorizer = TfidfVectorizer()
    job_tfidf = tfidf_vectorizer.fit_transform([" ".join([token.text for token in job_description_p])])
    resume_tfidf = tfidf_vectorizer.transform([" ".join(keywords) for keywords in resume_keywords])
    
    # Calculate cosine similarities
    similarities = cosine_similarity(job_tfidf, resume_tfidf)

    # Create a list of dictionaries with filename, title, and similarity score
    similarity_list = []
    for resume, similarity in zip(resumes, similarities[0]):
        similarity_dict = {
            'filename': resume.filename,
            'title': resume.title,
            'similarity_score': similarity
        }
        similarity_list.append(similarity_dict)

    # Sort the list by similarity scores (greatest to smallest)
    sorted_similarity_list = sorted(similarity_list, key=lambda item: item['similarity_score'], reverse=True)

    return sorted_similarity_list

def average_word_vectors(tokens, model, num_features):
    feature_vector = np.zeros((num_features,), dtype="float32")
    num_words = 0
    for token in tokens:
        if token in model:
            num_words += 1
            feature_vector = np.add(feature_vector, model[token])
    if num_words > 0:
        feature_vector = np.divide(feature_vector, num_words)
    return feature_vector

model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

def calculate_similarity_word2vec(job_description):
    job_description_tokens = job_description.split()
    job_description_vector = average_word_vectors(job_description_tokens, model, 300)

    # Get all resumes
    resumes = Resume.objects.all()
    
    similarity_list = []
    for resume in resumes:
        resume_text = resume.resume_text
        resume_tokens = resume_text.split()
        resume_vector = average_word_vectors(resume_tokens, model, 300)
        similarity = cosine_similarity([job_description_vector], [resume_vector])
        similarity_dict = {
            'filename': resume.filename,
            'title': resume.title,
            'similarity_score': similarity[0][0]
        }
        similarity_list.append(similarity_dict)
    
    # Sort the list by similarity scores (greatest to smallest)
    sorted_similarity_list = sorted(similarity_list, key=lambda item: item['similarity_score'], reverse=True)

    return sorted_similarity_list
    

