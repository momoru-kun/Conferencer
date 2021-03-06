from django.urls import re_path, path
from api.views import AllMembersToExcel, GetConferenceMembersExcel, GetConferencesExcel, SetApproval, GetAllMembers, Register, CheckUsername,GetConferenceMembers, ChangeStatus, DeleteConference, GetConfirence, AddMember, GetUser, AllConfirence, InsertConference

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


urlpatterns = [
    re_path(r'^user.token.obtain', obtain_jwt_token),
    re_path(r'^user.token.refresh', refresh_jwt_token),
    path('conference.get', GetConfirence.as_view()),
    path('conference.all', AllConfirence.as_view()),
    path('conference.add', InsertConference.as_view()),
    path('conference.delete', DeleteConference.as_view()),
    path('conference.activity', ChangeStatus.as_view()),
    path('conference.members', GetConferenceMembers.as_view()),
    path('member.add/', AddMember.as_view()),
    path('member.all', GetAllMembers.as_view()),
    path('member.approve', SetApproval.as_view()),
    path('user.get', GetUser.as_view()),
    path('user.check', CheckUsername.as_view()),
    path('user.register', Register.as_view()),
    path('export.conferences', GetConferencesExcel.as_view()),
    path('export.conferenceMembers', GetConferenceMembersExcel.as_view()),
    path('export.allMembers', AllMembersToExcel.as_view())
]
urlpatterns += staticfiles_urlpatterns()