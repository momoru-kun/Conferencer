from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.renderers import TemplateHTMLRenderer

from api.models import Conference

# Create your views here.
class AdminPanel(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    
    def get(self, response):
        return Response(template_name="admin.html")

class Quiz(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    
    def get(self, response, conf_id):
        get_object_or_404(Conference, pk=conf_id)
        return Response({'c_id': conf_id}, template_name="quiz.html")

class Index(APIView):
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, response):
        return Response(template_name="index.html")

