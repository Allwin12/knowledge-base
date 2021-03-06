from rest_framework import serializers
from .models import Category, DocumentFile, KnowledgeBase


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentFile
        fields = '__all__'


class DocumentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentFile
        fields = ['id', 'doc_id', 'category', 'doc_type', 'question', 'answer', 'title', 'content']


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeBase
        fields = '__all__'
        extra_kwargs = {"customers": {"allow_empty": True}}


class CategoryDetailSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'documents']

    def get_documents(self, instance):
        return DocumentViewSerializer(DocumentFile.objects.filter(category=instance.pk), many=True).data,
