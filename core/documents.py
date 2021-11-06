from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import DocumentFile


@registry.register_document
class CategoryDocument(Document):
    class Index:
        name = 'documents'

    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }
    es_id = fields.TextField(attr="es_id")

    class Django:
        model = DocumentFile
        fields = [
            'id',
            'doc_id',
            'doc_type',
            'question',
            'answer',
            'title',
            'content'
        ]


