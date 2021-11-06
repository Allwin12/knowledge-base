from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class KnowledgeBase(models.Model):
    ENGLISH = 'ENGLISH'
    SPANISH = 'SPANISH'
    LANGUAGES = ((ENGLISH, 'English'),
                 (SPANISH, 'Spanish'))

    description = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    language = models.CharField(choices=LANGUAGES, default=ENGLISH, max_length=50)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='author')
    customers = models.ManyToManyField('users.User', limit_choices_to={'role': 'CUSTOMER'}, related_name='customers')

    def __str__(self):
        return f"{self.pk} - {self.description}"


class DocumentFile(models.Model):
    FAQ = 'FAQ'
    ARTICLE = 'ARTICLE'
    DOC_TYPE = ((FAQ, 'FAQ'),
                (ARTICLE, 'Article'))

    doc_id = models.CharField(max_length=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    doc_type = models.CharField(choices=DOC_TYPE, max_length=10)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    question = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.doc_id} {self.doc_type}"

    def es_id(self):
        return str(self.pk)
