import json

from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import DocumentFile
from .serializers import DocumentSerializer


class FileUtil(object):
    def __init__(self, file: InMemoryUploadedFile):
        self.file = file

    def parse_file(self, category):
        document_data = {
        }

        data = json.load(self.file)
        doc_id = data.get('DocId')
        doc_type = data.get('DocType')
        document_data['doc_id'] = doc_id
        document_data['doc_type'] = doc_type
        document_data['category'] = category

        if doc_type == DocumentFile.FAQ:
            document_data.update({
                'question': data.get('Question', ''),
                'answer': data.get('Answer', '')
            })
        else:
            document_data.update({
                'title': data.get('Title', ''),
                'content': data.get('Content', '')
            })
        document = DocumentSerializer(data=document_data)
        if document.is_valid():
            document.save()
