"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from evoting import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('log',views.log),
    path('logpost',views.logpost),
    path('useradd',views.useradd),
    path('useraddpost',views.useraddpost),
    path('useredit/<id>',views.useredit),
    path('usereditpost/<id>',views.usereditpost),
    path('userview',views.userview),
    path('rules',views.rulesadd),
    path('rulespost',views.rulespost),
    path('editrules/<id>',views.editrules),
    path('editrulespost/<id>',views.editrulespost),
    path('rules1',views.rules1),
    path('candidateview/<id>',views.candidateview),
    path('postview',views.postview),
    path('postadd',views.postadd),
    path('postaddpost',views.postaddpost),
    path('editpost/<id>',views.editpost),
    path('posteditpost/<id>',views.posteditpost),
    path('electionadd',views.electionadd),
    path('electionpost',views.electionpost),
    path('electionedit/<id>',views.electionedit),
    path('electioneditpost/<id>',views.electioneditpost),
    path('election1',views.election1),
    path('view_coordinators',views.view_coordinators),
    path('complaint',views.complaint),
    path('changepswd',views.changepswd),
    path('changepswdpost',views.changepswdpost),
    path('adminhome',views.adminhome),
    path('userdelete/<id>',views.userdelete),
    path('rulesdelete/<id>',views.rulesdelete),
    path('postdelete/<id>', views.postdelete),
    path('electiondelete/<id>', views.electiondelete),
    path('acceptcan/<id>/<em>', views.acceptcan),
    path('forward/<id>/<em>', views.forward),
    path('rejectcan/<id>/<em>', views.rejectcan),
    path('userinfo', views.userinfo),
    path('sendreplay/<id>', views.sendreplay),
    path('sendreplaypost/<id>', views.sendreplaypost),
    path('sendreason/<id>/<em>', views.sendreason),
    path('sendreasonpost/<id>/<em>', views.sendreasonpost),
    path('results', views.results),
    path('logout2', views.logout),
    path('studentview', views.studentview),
    path('allvoteduser', views.allvoteduser),
    path('eresults', views.eresults),
    # ==
path('deptadd', views.deptadd),
path('deptadd_post', views.deptadd_post),
path('view_dept', views.view_dept),
path('delete_dept/<id>', views.delete_dept),
path('courseadd', views.courseadd),
path('courseadd_post', views.courseadd_post),
path('view_course', views.view_course),
path('delete_course/<id>', views.delete_course),
path('remove_coor/<id>', views.remove_coor),
path('candidateviewe/<id>', views.candidateviewe),

    #---------------------------------------------------------------------------
    # path('addcampaign', views.addcampaign),
    # path('addcampaignpost', views.addcampaignpost),
    # path('candidatehome', views.candidatehome),
    # path('viewcampaign', views.viewcampaign),
    # path('viewcampaignothers/<id>', views.viewcampaignothers),
    # path('campaigndelete/<id>', views.campaigndelete),
    # path('viewcandidates/<id>', views.viewcandidates),
    # path('viewpost', views.viewpost),
    # path('viewresult', views.viewresult),
    # path('viewuser', views.viewuser),
    # path('changepassword', views.changepassword),
    # path('changepswdpost1',views.changepswdpost1),
    # path('logout1',views.logout1),

#---------------------------------------------------------------------------------

    path('and_login', views.and_login),
    path('addimg', views.addimg),
    path('and_election', views.and_election),
    path('and_post', views.and_post),
    path('and_rule', views.and_rule),
    path('changepswdpost2',views.changepswdpost2),
    path('sendcomplaint',views.sendcomplaint),
    path('sendcomplaintpost',views.sendcomplaintpost),
    path('viewcampaign1/<id>',views.viewcampaign1),
    path('viewcandidate1/<id>',views.viewcandidate1),
    path('viewcandidates1/<id>/<eid>',views.viewcandidates1),
    path('studenthome',views.studenthome),
    path('viewelection',views.viewelection),
    path('sendreview',views.sendreview),
    path('sendreviewpost',views.sendreviewpost),
    path('viewcomplaint',views.viewcomplaint),
    path('viewresultmore/<id>/<i>',views.viewresultmore),
    path('viewresult1/<id>',views.viewresult1),
    path('viewrule1',views.viewrule1),
    path('viewpost1/<id>',views.viewpost1),
    path('applyascandidate/<postid>/<eid>',views.applyascandidate),
    path('applyascandidatepost',views.applyascandidatepost),
    path('and_view_nominees',views.and_view_nominees),
    path('and_complaint',views.and_complaint),
    path('and_view_reply',views.and_view_reply),
    path('and_verification',views.and_verification),


    path('voting',views.voting),
    path('votingpost',views.votingpost),
    path('otp',views.otp1),
    path('otppost',views.otppost),
    path('votingpage',views.votingpage),
    path('vote',views.votes),
    path('uviewresult',views.uviewresult),


    path('forgo',views.forgo),
    path('forpost',views.forpost),

# =================================================
path('coordinator_home',views.coordinator_home),
path('evcomplaint',views.evcomplaint),
path('coordreg',views.coordreg),
path('candidateviewe',views.candidateviewe),
path('admin_election',views.admin_election),



]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
