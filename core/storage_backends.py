# core/storage_backends.py
from supabase import create_client
from django.core.files.storage import Storage
from django.core.files.base import ContentFile

class SupabaseStorage(Storage):
    def __init__(self):
        url = "https://psboxeqyrgmzienrsvhf.supabase.co"  # remplace par ton URL
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzYm94ZXF5cmdtemllbnJzdmhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgwNzM0OTEsImV4cCI6MjA4MzY0OTQ5MX0.GK86ZOdBueEhDupbrjHbUYABg4-Mq1O_Zw7slgxU_e0"                     # remplace par ta clé
        self.client = create_client(url, key)
        self.bucket = "media"  # nom de ton bucket Supabase

    def _save(self, name, content):
        # upload sur Supabase
        data = content.read()
        self.client.storage.from_(self.bucket).upload(name, data)
        return name

    def url(self, name):
        # URL publique du fichier
        return self.client.storage.from_(self.bucket).get_public_url(name)
