from django.apps import AppConfig
import spacy


class ResumesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resumes'

    nlp = spacy.load("en_core_web_sm")
