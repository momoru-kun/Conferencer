from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status, parsers
from rest_framework.renderers import JSONRenderer

from api.models import Conference, Member
from api.serializers import UserSerializer

# USERS SECTION
class GetUser(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.JSONParser,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CheckUsername(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.JSONParser,)

    def post(self, request):
        get_object_or_404(User, username=request.data['login'])
        
        return Response({'status': 'ok', 'user': True})


class Register(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.JSONParser,)

    def post(self, request):
        login = request.data.get('login', None)
        password = request.data.get('password', None)
        email = request.data.get('email', None)
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        if login == None:
            return Response(data={'status': 'error', 'error_description': 'username required'})
        if password == None:
            return Response(data={'status': 'error', 'error_description': 'password required'})
        if email == None:
            return Response(data={'status': 'error', 'error_description': 'email required'})
        if first_name == None:
            return Response(data={'status': 'error', 'error_description': 'first_name required'})
        if last_name == None:
            return Response(data={'status': 'error', 'error_description': 'last_name required'})
        
        if len(User.objects.filter(username=request.data['login'])) != 0:
            return Response(data={'status': 'error', 'error_description': 'username already taken'})
        
        u = User(
            username=login, 
            email=email, 
            first_name=first_name,
            last_name=last_name
        )

        u.set_password(password)

        u.save()

        return Response({'status': 'ok', 'user_id': u.id})

# CONFERENCES SECTION
class GetConfirence(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, response):
        id_ = response.data['id']
        c = Conference.objects.get(pk=id_)

        return Response({'status': "ok", "response": [{"id": c.pk, "name": c.name, "status": c.active}]}, status=status.HTTP_200_OK)


class AllConfirence(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        serializer = UserSerializer(request.user)
        id_ = serializer.data['id']

        conferences = User.objects.get(pk=id_).conference_set.all()
        response = {'status': 'ok', 'response': []}
        for conf in conferences:
            response['response'].append({'id': conf.id, 'name': conf.name, 'active': conf.active, 'count': conf.member_set.count()})
        return Response(data=response, status=status.HTTP_200_OK)


class InsertConference(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (JSONRenderer,)

    def get(self, response):
        id_ = response.GET['id']

        if id_ == "all": 
            confs = Conference.objects.all()
            resp = []
            for c in confs:
                resp.append({"id": c.pk, "name": c.name, "status": c.active})
            
            return Response({'status': 'ok', 'response': resp}, status=status.HTTP_200_OK)
        else:    
            c = Conference.objects.get(pk=id_)

            return Response({'status': "ok", "response": [{"id": c.pk, "name": c.name, "status": c.active}]}, status=status.HTTP_200_OK)
    
    def post(self, request):
        name = request.data['name']

        serializer = UserSerializer(request.user)
        id_ = serializer.data['id']
        u = User.objects.get(pk=id_)
        c = u.conference_set.create(name=name)
        u.save()

        return Response({"status": "ok", "conference_id": c.id}, status=status.HTTP_200_OK)


class DeleteConference(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        serializer = UserSerializer(request.user)
        id_ = serializer.data['id']
        u = User.objects.get(pk=id_)

        c = u.conference_set.get(pk=request.data['conf_id'])
        
        c.delete()

        return Response({"status": "ok"})


class ChangeStatus(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        serializer = UserSerializer(request.user)
        id_ = serializer.data['id']
        u = User.objects.get(pk=id_)

        c = u.conference_set.get(pk=request.data['conf_id'])
        
        c.active = not c.active
        c.save()

        return Response({"status": "ok"})

# MEMBERS SECTION
class AddMember(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        id_ = request.data.get('conf_id', None)

        if id_ == None:
            return Response({"status": "error", "error_description": "Field 'id' is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        c = get_object_or_404(Conference, pk=id_)

        form = request.data.get('form', None)

        if form == None:
            return Response({"status": "error", "error_description": "Field 'form' is required"}, status=status.HTTP_400_BAD_REQUEST)

        m = Member(
            name=form.get('name'), 
            surname=form.get('surname'), 
            middlename=form.get('middlename'), 
            email=form.get('email'), 
            city=form.get('city'), 
            uni=form.get('uni'),
            course=form.get('study'),
            with_topic=form.get('topic'), 
            topic=form.get('topicSubject')
        )

        c.member_set.add(m, bulk = False)

        return Response({"status": "ok", "member_id": m.pk})


class GetConferenceMembers(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        serializer = UserSerializer(request.user)
        id_ = serializer.data['id']
        u = User.objects.get(pk=id_)

        members = [member.to_dict() for member in u.conference_set.get(pk=request.data['conf_id']).member_set.all()]

        return Response({"status": "ok", "response": members})