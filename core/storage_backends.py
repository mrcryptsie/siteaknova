# core/storage_backends.py

from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client
from django.conf import settings
import os

class SupabaseStorage(Storage):
    """
    Django Storage backend pour Supabase
    Compatible Django 5 / Vercel / Admin
    """

    def __init__(self):
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_ANON_KEY")

        if not supabase_url.endswith("/"):
            supabase_url += "/"

        self.client = create_client(supabase_url, supabase_key)
        self.bucket = "media"

    def _save(self, name, content):
        data = content.read()

        # ⚠️ upsert DOIT être un paramètre nommé
        self.client.storage.from_(self.bucket).upload(
            path=name,
            file=data,
            file_options={"upsert": "true"}  # STRING, pas bool
        )

        return name

    def exists(self, name):
        # Django ne doit jamais bloquer l’upload
        return False

    def url(self, name):
        return self.client.storage.from_(self.bucket).get_public_url(name)

    def open(self, name, mode="rb"):
        data = self.client.storage.from_(self.bucket).download(name)
        return ContentFile(data)
