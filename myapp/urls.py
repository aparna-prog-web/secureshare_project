
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('login_get/',views.login_get),
    path('login_post/',views.login_post),
    path('change_password/',views.change_password),
    path('change_password_post/',views.change_password_post),
    path('send_reply/<id>',views. send_reply),
    path('sent_reply_post/',views. sent_reply_post),
    path('view_review/',views.view_review),
    path('view_complaint/',views.view_complaint),
    path('view_user/',views.view_user),
    path('adminhome/',views.adminhome),
    path('logout_get/',views.logout_get),
    path('userview_allrequest/',views.userview_allrequest),
    path('userview_requeststatus/',views.userview_requeststatus),
    path('userviewmy_post/',views.userviewmy_post),
    path('addeducationalcontent_get/',views.addeducationalcontent_get),
    path('addeducationalcontent_post/',views.addeducationalcontent_post),
    path('editeducationalcontent_get/<id>',views.editeducationalcontent_get),
    path('editeducationalcontent_post/',views.editeducationalcontent_post),
    path('vieweducationalcontent_get/',views.vieweducationalcontent_get),
    path('deleteeducationalcontent_get/<id>',views.deleteeducationalcontent_get),
    path('forgetpassword_get/',views.forgetpassword_get),
    path('forgetpassword_post/',views.forgetpassword_post),







    path('viewOwnpost_comment/',views.viewOwnpost_comment),
    path('user_deletecomment/',views.user_deletecomment),
    path('user_allpost_deletecomment/',views.user_allpost_deletecomment),


    path('user_signup_post/',views.user_signup_post),
    path('user_view_profile/',views.user_view_profile),
    path('user_login_post/',views.user_login_post),
    path('viewusers/',views.viewusers),
    path('usereditprofile/',views.usereditprofile),
    path('userchangepassword/',views.userchangepassword),
    path('add_post/',views.add_post),
    path('add_video/',views.add_video),
    path('sendrequest/',views.sendrequest),
    path('accept_request/',views.accept_request),
    path('reject_request/',views.reject_request),
    path('view_friendprofile/',views.view_friendprofile),
    path('add_add_post/',views.add_post),
    path('user_deletepost/',views.user_deletepost),
    path('userviewall_post/',views.userviewall_post),
    path('likepost/',views.likepost),
    path('addcomment/',views.addcomment),
    path('viewcomment/',views.viewcomment),
    path('sendcomplaint/',views.sendcomplaint),
    path('viewreply/',views.viewreply),
    path('sendappreview/',views.sendappreview),
    path('viewreview/',views.viewreview),
    path('chat_view/',views.chat_view),
    path('chat_send/',views.chat_send),
    path('User_sendchat/',views.User_sendchat),
    path('User_viewchat/',views.User_viewchat),
    path('android_forget_password/',views.android_forget_password),

    path('userviewmy_notifications/',views.userviewmy_notifications),
    path('accept_notification/',views.accept_notification),
    path('reject_notification/',views.reject_notification),
    path('viewNotification/',views.viewNotification),






]
