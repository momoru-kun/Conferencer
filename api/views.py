from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status, parsers
from rest_framework.renderers import JSONRenderer

from api.models import Conference, Member
from api.serializers import UserSerializer
from confregistration.FileRenderer import FileRenderer 
from confregistration.settings import EMAIL_HOST_USER

from time import time

import pandas as pd
import base64
import os

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
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        serializer = UserSerializer(request.user)
        id_ = serializer.data['id']
        u = User.objects.get(pk=id_)

        members = [member.to_dict() for member in u.conference_set.get(pk=request.data['conf_id']).member_set.all()]

        return Response({"status": "ok", "response": members})


class GetAllMembers(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        serializer = UserSerializer(request.user)
        id_ = serializer.data['id']
        u = User.objects.get(pk=id_)

        conferences = u.conference_set.all()

        members = []
        for conf in conferences:
            for member in conf.member_set.all():
                member = member.to_dict()
                member['conf_name'] = conf.name
                member['conf_id'] = conf.id

                members.append(member)

        return Response({"status": "ok", "response": members})


class SetApproval(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        serializer = UserSerializer(request.user)
        id_ = serializer.data['id']
        u = User.objects.get(pk=id_)

        conf_id = request.data.get('conf_id', None)
        if conf_id == None:
            return Response(data={"status": "error", "error_description": "`conf_id` field is required"}, status=status.HTTP_400_BAD_REQUEST)

        member_id = request.data.get('member_id', None)
        if member_id == None:
            return Response(data={"status": "error", "error_description": "`member_id` field is required"}, status=status.HTTP_400_BAD_REQUEST)


        conference = None
        try:
            conference = u.conference_set.get(pk=conf_id)
        except:
            return Response(data={"status": "error", "error_description": "Couldn't found conference"}, status=status.HTTP_400_BAD_REQUEST)
        
        member = None
        try:
            member = conference.member_set.get(pk=member_id)
        except:
            return Response(data={"status": "error", "error_description": "Couldn't found member"}, status=status.HTTP_400_BAD_REQUEST)
    
        approved = request.data.get('approved', None)
        if approved == None:
            return Response(data={"status": "error", "error_description": "`approved` field is required"}, status=status.HTTP_400_BAD_REQUEST)
        member.approved = approved
        member.save()

        try:
            if member.approved:
                send_mail(
                    subject="Подтверждение участия на конференции {}".format(conference.name),
                    from_email= EMAIL_HOST_USER,
                    recipient_list = [member.email],
                    message= "Поздравляем! Вашу личность подтвердили на участие в конференции '{}'".format(conference.name)
                )
            else:
                send_mail(
                    subject="Подтверждение участия на конференции {}".format(conference.name),
                    from_email= EMAIL_HOST_USER,
                    recipient_list = [member.email],
                    message= "К сожалению, организатор не подтвердил вас на участие в конференции '{}'".format(conference.name)
                )
        except:
            pass

        return Response({"status": "ok"})


# EXPORT SECTION
class GetConferencesExcel(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        id_ = serializer.data['id']
        u = User.objects.get(pk=id_)

        conferences = u.conference_set.all()

        table = {
            'Название': [],
            'Подали заявку': [],
            'Идёт набор': []
        }

        for conf in conferences:
            table['Название'].append(conf.name)
            table['Подали заявку'].append(conf.member_set.count())
            table['Идёт набор'].append("Да" if conf.active else "Нет")

        filename = './{}.xlsx'.format(hex(int(time() * 1000)))

        df = pd.DataFrame(table)
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        df.to_excel(writer, startrow = 1, sheet_name='Конференции', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Конференции']

        for i, col in enumerate(df.columns):
            column_len = df[col].astype(str).str.len().max()
            column_len = max(column_len, len(col)) + 2
            worksheet.set_column(i, i, column_len)

        writer.save()

        file_data = open(filename, 'rb').read()

        os.remove(filename)

        return Response({'status': 'ok', 'data': base64.b64encode(file_data)})


class GetConferenceMembersExcel(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        id_ = serializer.data['id']
        u = User.objects.get(pk=id_)

        conf_id = request.GET.get('conf_id', None)
        if conf_id == None:
            return Response({"status": "error", "error_description": "Field 'conf_id' is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        conference = u.conference_set.get(pk=conf_id)

        table = {
            "Фамилия": [],
            "Имя": [],
            "Отчество": [],
            "E-mail": [],
            "Город": [],
            "Учебное заведение": [],
            "Направление": [],
            "Выступает с докладом": [],
            "Тема доклада": [],
            "Подтверждён": [],
        }

        for member in conference.member_set.all():
            approval = "-"
            if member.approved == None:
                approval = "Не подтверждён"
            elif member.approved == True:
                approval = "Подтверждён"
            elif member.approved == False:
                approval = "Отклонён"
            table['Фамилия'].append(member.surname)
            table['Имя'].append(member.name)
            table['Отчество'].append(member.middlename)
            table['E-mail'].append(member.email)
            table['Город'].append(member.city)
            table['Учебное заведение'].append(member.uni)
            table['Направление'].append(member.course)
            table['Выступает с докладом'].append("Да" if member.with_topic else "Нет")
            table['Тема доклада'].append(member.topic)
            table['Подтверждён'].append(approval)

        filename = './{}.xlsx'.format(hex(int(time() * 1000)))

        df = pd.DataFrame(table)
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        df.to_excel(writer, startrow = 1, startcol = 1, sheet_name='Участники', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Участники']

        worksheet.write(0, 0, conference.name)
        worksheet.set_column(0, 0, len(conference.name)+20)

        for i, col in enumerate(df.columns):
            column_len = df[col].astype(str).str.len().max()
            column_len = max(column_len, len(col)) + 10
            worksheet.set_column(i, i, column_len)

        writer.save()

        file_data = open(filename, 'rb').read()

        os.remove(filename)

        return Response({'status': 'ok', 'data': base64.b64encode(file_data)})

class AllMembersToExcel(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        id_ = serializer.data['id']
        u = User.objects.get(pk=id_)

        conferences = u.conference_set.all()

        table = {
            "Фамилия": [],
            "Имя": [],
            "Отчество": [],
            "Конференция": [],
            "E-mail": [],
            "Город": [],
            "Учебное заведение": [],
            "Направление": [],
            "Выступает с докладом": [],
            "Тема доклада": [],
            "Подтверждён": [],
        }

        for conference in conferences:
            for member in conference.member_set.all():
                approval = "-"
                if member.approved == None:
                    approval = "Не подтверждён"
                elif member.approved == True:
                    approval = "Подтверждён"
                elif member.approved == False:
                    approval = "Отклонён"
                table['Фамилия'].append(member.surname)
                table['Имя'].append(member.name)
                table['Отчество'].append(member.middlename)
                table['E-mail'].append(member.email)
                table['Город'].append(member.city)
                table['Учебное заведение'].append(member.uni)
                table['Направление'].append(member.course)
                table['Выступает с докладом'].append("Да" if member.with_topic else "Нет")
                table['Тема доклада'].append(member.topic)
                table['Подтверждён'].append(approval)
                table['Конференция'].append(conference.name)

        filename = './{}.xlsx'.format(hex(int(time() * 1000)))

        df = pd.DataFrame(table)
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        df.to_excel(writer, startrow = 0, startcol = 0, sheet_name='Участники всех конференций', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Участники всех конференций']

        for i, col in enumerate(df.columns):
            column_len = df[col].astype(str).str.len().max()
            column_len = max(column_len, len(col)) + 10
            worksheet.set_column(i, i, column_len)

        writer.save()

        file_data = open(filename, 'rb').read()

        os.remove(filename)

        return Response({'status': 'ok', 'data': base64.b64encode(file_data)})