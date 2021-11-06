from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from backend.permissions import IsAuthor
from backend.swagger_utils import RequiredQueryParam
from .documents import CategoryDocument
from .models import Category, DocumentFile, KnowledgeBase
from .serializers import CategorySerializer, DocumentViewSerializer, KnowledgeBaseSerializer
from .utils import FileUtil


def get_generic_error_schema():
    return openapi.Schema(
        'Generic API Error',
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details'),
            'code': openapi.Schema(type=openapi.TYPE_STRING, description='Error code'),
        },
        required=['detail']
    )


def get_validation_error_schema():
    return openapi.Schema(
        'Validation Error',
        type=openapi.TYPE_OBJECT,
        properties={
            "errors": openapi.Schema(
                description='List of validation errors not related to any field',
                type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)
            ),
        }
    )


class KnowledgeBaseView(GenericAPIView):
    serializer_class = KnowledgeBaseSerializer
    model = KnowledgeBase

    @swagger_auto_schema(tags=['Knowledge Base'], operation_summary="Add New Knowledge Base",
                         responses={422: get_validation_error_schema()})
    def post(self, request):
        body = request.data
        knowledge_base = self.serializer_class(data=body)
        if knowledge_base.is_valid():
            knowledge_base.save()
            return Response(knowledge_base.data, status=201)
        return Response(knowledge_base.errors, status=422)

    params = RequiredQueryParam(
        [('locale', str, "Document Language"), ('category_id', str, 'comma separated category ids')]).params

    @swagger_auto_schema(manual_parameters=params, tags=['Knowledge Base'], operation_summary="List Knowledge Bases")
    def get(self, request):
        locale = request.GET.get('locale')
        category_id = request.GET.get('category_id')
        queryset = self.model.objects.all()

        if locale:
            queryset = queryset.filter(language=locale)
        if category_id:
            category_id = category_id.split(',')
            queryset = queryset.filter(categories__in=category_id)
        return self.get_paginated_response(self.paginate_queryset(self.serializer_class(queryset, many=True).data))


class CategoryView(GenericAPIView):
    serializer_class = CategorySerializer
    model = Category

    @swagger_auto_schema(tags=['Category'], operation_summary="Add New Category")
    def post(self, request):
        category = self.serializer_class(data=request.data)
        if category.is_valid():
            category.save()
            return Response(category.data, 201)
        return Response(category.errors, 422)

    @swagger_auto_schema(tags=['Category'], operation_summary="List Categories")
    def get(self, request):
        categories = self.model.objects.all()
        return self.get_paginated_response(self.paginate_queryset(self.serializer_class(categories, many=True).data))


class DocumentUploadView(GenericAPIView):
    serializer_class = None
    parser_classes = (MultiPartParser,)
    files = openapi.Parameter(name='files', in_=openapi.IN_FORM, type=openapi.TYPE_FILE)
    category = openapi.Parameter(name='category', in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[files, category], operation_summary="Upload Document", tags=['Document'])
    def post(self, request):
        files = request.FILES.getlist('files')
        category = request.data.get('category')
        for file in files:
            FileUtil(file).parse_file(category)
        return Response(status=200)


class DocumentView(GenericAPIView):
    model_class = DocumentFile
    serializer_class = DocumentViewSerializer
    permission_classes = [IsAuthor]

    @swagger_auto_schema(operation_summary="Upload Document", tags=['Document'])
    def get(self, request):
        doc_type = request.GET.get('doc_type')
        search = request.GET.get('search')
        elastic_search = request.GET.get('es', False)

        documents = self.model_class.objects.all()
        if doc_type:
            documents = documents.filter(doc_type=doc_type)
        if search:
            if elastic_search:
                query = {
                    "multi_match": {
                        "query": search,
                        "fields": ["doc_id", "doc_type", "question", "answer", "title", "content", "es_id"],
                        "type": "phrase_prefix"
                    }
                }
                documents = CategoryDocument.search().query(query).sort('-id').to_queryset()
            else:
                documents = documents.filter(Q(doc_type__icontains=search) | Q(doc_id__icontains=search) |
                                             Q(title__icontains=search) | Q(content__icontains=search) |
                                             Q(question__icontains=search) | Q(answer__icontains=search))
        return self.get_paginated_response(self.paginate_queryset(self.serializer_class(documents, many=True).data))
