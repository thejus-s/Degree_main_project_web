import datetime
import random
import smtplib
from email.mime.text import MIMEText

from django.core.files.storage import FileSystemStorage
from django.db.models import Q, Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from evoting.encode_faces import enf
from evoting.models import *
from evoting.recognize_face import rec_face_image


def index(request):
    import datetime
    t = datetime.datetime.now().strftime("%H")
    print(int(t[1]) >= 9 and int(t[1]),t)
    if int(t[1]) >= 9 and int(t) <= 14:
        e = election.objects.filter(votingdate=datetime.datetime.now().date())
        if e.exists():
            request.session['eid'] = e[0].id
            return render(request, "index.html",{"data":1})
        else:
            return render(request,"index.html",{"data":0})
    elif int(t) >= 10 and int(t) <= 14:
        e = election.objects.filter(votingdate=datetime.datetime.now().date())
        if e.exists():
            request.session['eid'] = e[0].id
            return render(request, "index.html", {"data": 1})
        else:
            return render(request, "index.html", {"data": 0})
    else:
        return render(request, "index.html", {"data": 0})

def log(request):
    return render(request,"newindex.html")

def logout2(request):
    return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

def logpost(request):
    un = request.POST['textfield']
    p = request.POST['textfield2']
    l = login.objects.filter(username=un,password=p)
    if l.exists():
        l = l[0]
        request.session['lid']=l.id
        request.session['lin'] = "1"
        if l.usertype == 'admin':
            return HttpResponse('<script>alert("welcome admin");window.location ="/adminhome"</script>')
        elif l.usertype == 'candidate':
            request.session['cid']=candidatelogin.objects.get(LOGIN=l.id).CANDIDATE_id
            return HttpResponse('<script>alert("welcome candidate");window.location ="/candidatehome"</script>')
        elif l.usertype == 'user':
            request.session['uid']=user.objects.get(LOGIN=l.id).id
            return HttpResponse('<script>alert("welcome user");window.location ="/studenthome"</script>')
        elif l.usertype == 'election_coordinator':
            request.session['eid']=election_coordinator.objects.get(LOGIN=l.id).id
            return HttpResponse('<script>alert("welcome Coordinator");window.location ="/coordinator_home"</script>')

        else:
            return HttpResponse('<script>alert("your account is blocked");window.location ="/"</script>')
    else:
        return HttpResponse('<script>alert("admin does not exists");window.location ="/"</script>')

def useradd(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')
    request.session['h']="ADD STUDENT"
    data = course.objects.all()
    print(data,"iiii")
    return render(request,"admin/User add.html",{"data":data})
def useraddpost(request):
    N = request.POST['textfield']
    c = request.POST['select']
    s = request.POST['select2']
    y = request.POST['select3']
    p = request.FILES['f']
    import datetime
    d = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    fs = FileSystemStorage()
    # fs.save(r"D:\untitled\untitled\evoting\static\\"+d+'.jpg',p)
    fn=fs.save(p.name,p)


    us = request.POST['textfield2']
    pd = random.randint(0000,9999)
    if login.objects.filter(username=us).exists():
        return HttpResponse('<script>alert("data already exists");window.location ="/useradd#home"</script>')
    lobj = login()
    lobj.username = us
    lobj.password = pd
    lobj.usertype = 'user'
    lobj.save()


    uobj = user()
    uobj.name = N
    uobj.course = c
    uobj.sem = s
    uobj.year = y
    uobj.LOGIN = lobj
    # uobj.photo='/static/'+d+'.jpg'
    uobj.photo=fn
    uobj.email = us
    uobj.save()

    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)

        gmail.ehlo()

        gmail.starttls()

        gmail.login('onlinevotingbca@gmail.com', 'nkba zott ofxx rxad')

    except Exception as e:
        print("Couldn't setup email!!" + str(e))

    msg = MIMEText("Your password is " + str(pd))

    msg['Subject'] = 'Verification'

    msg['To'] = us

    msg['From'] = 'onlinevotingbca@gmail.com'

    try:

        gmail.send_message(msg)

    except Exception as e:

        print("COULDN'T SEND EMAIL", str(e))
    return  HttpResponse('<script>alert("Added successfully");window.location ="/useradd#home"</script>')
def useredit(request,id):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')
    data = user.objects.get(id = id)
    request.session['h'] = "EDIT STUDENT"
    return render(request,"admin/User edit.html",{"data":data})
def usereditpost(request,id):
    N = request.POST['textfield']

    s = request.POST['select2']
    y = request.POST['select3']
    if 'f' in  request.FILES:
        p = request.FILES['f']

        import datetime
        d = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        fs = FileSystemStorage()
        fs.save(r"C:\Users\Adarsh\OneDrive\Desktop\untitled\untitled\evoting\static\\" + d + '.jpg', p)
        user.objects.filter(id = id ).update(photo = '/static/'+d+'.jpg')
    user.objects.filter(id = id ).update(name = N,sem = s,year = y)

    return  HttpResponse('<script>alert("update successfull");window.location ="/userview#home"</script>')
def userview(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "STUDENT"
    data = user.objects.all()
    return render(request,"admin/User view.html",{"data":data})

def studentview(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    cr = request.POST['select']
    yr = request.POST['select3']
    data = user.objects.filter(course=cr,year=yr)

    return render(request, "admin/User view.html",{"data":data})

def userdelete(request,id):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    user.objects.get(id = id).delete()
    return HttpResponse('<script>alert("delete successfull");window.location ="/userview#home"</script>')

# =dept

def deptadd(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "ADD DEPARMENT"
    return render(request,"admin/add_dept.html")
def deptadd_post(request):
    T = request.POST['textfield']
    if department.objects.filter(dept=T, ).exists():
        return HttpResponse('<script>alert("data already exists");window.location ="/deptadd#home"</script>')
    robj = department()
    robj.dept = T

    robj.save()
    return HttpResponse('<script>alert("Added successfully");window.location ="/view_dept#home"</script>')

def view_dept(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "DEPARMENT"
    data=department.objects.all()
    return render(request,"admin/view_dept.html",{"data":data})


def delete_dept(request,id):
    department.objects.get(id = id).delete()
    return HttpResponse('<script>alert("delete successfull");window.location ="/view_dept#home"</script>')

# ===course

def courseadd(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')
    qry=department.objects.all()
    request.session['h'] = "ADD COURSE"
    return render(request,"admin/add_course.html",{"data":qry})
def courseadd_post(request):
    d = request.POST['t']
    T = request.POST['textfield']
    # if department.objects.filter(dept=T, ).exists():
    #     return HttpResponse('<script>alert("data already exists");window.location ="/deptadd#home"</script>')
    robj = course()
    robj.DEPARTMENT_id = d
    robj.coursename=T
    robj.save()
    return HttpResponse('<script>alert("Added successfully");window.location ="/view_course#home"</script>')

def view_course(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "COURSES"
    data=course.objects.all()
    return render(request,"admin/view_course.html",{"data":data})


def delete_course(request,id):
    course.objects.get(id = id).delete()
    return HttpResponse('<script>alert("delete successfull");window.location ="/view_course#home"</script>')

def rulesadd(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "ADD RULES"
    return render(request,"admin/Rules.html")
def rulespost(request):
    T = request.POST['textfield']
    dis = request.POST['textarea']
    if rules.objects.filter(title=T, ).exists():
        return HttpResponse('<script>alert("data already exists");window.location ="/rulesadd#home"</script>')
    robj = rules()
    robj.title = T
    robj.description=dis

    robj.save()
    return HttpResponse('<script>alert("Added successfully");window.location ="/rules#home"</script>')
def editrules(request,id):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "EDIT RULES"
    data = rules.objects.get(id=id)
    return render(request,"admin/Edit Rules.html",{"data":data})
def editrulespost(request,id):
    T = request.POST['textfield']
    dis = request.POST['textarea']
    rules.objects.filter(id=id).update(title=T, description=dis)
    return  HttpResponse('<script>alert("update successfull");window.location ="/rules1#home"</script>')
def rules1(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "RULES"
    data=rules.objects.all()
    return render(request,"admin/Rules 1.html",{"data":data})
def rulesdelete(request,id):
    rules.objects.get(id = id).delete()
    return HttpResponse('<script>alert("delete successfull");window.location ="/rules1#home"</script>')


def candidateview(request,id):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "CANDIDATES"
    request.session['eid']=id
    data = candidates.objects.filter(Q(ELECTION=id)& (Q(status="forwarded") | Q(status="approved")))
    return render(request,"admin/View reg candiates.html",{"data":data})
def acceptcan(request,id,em):
    q = candidates.objects.filter(id=id)
    q2=q.update(status = 'approved')
    p = random.randint(0000,9999)
    obj = login()
    obj.username = q[0].USER.email
    obj.password = p
    obj.usertype = 'candidate'
    obj.save()
    obj2 = candidatelogin()
    obj2.CANDIDATE_id=q[0].id
    obj2.LOGIN = obj
    obj2.save()

    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)

        gmail.ehlo()

        gmail.starttls()

        gmail.login('onlinevotingbca@gmail.com', 'nkba zott ofxx rxad')

    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    message ='''
        <pre>
        Your Candidate request accepted<br>
        Your password for candidate panel is  
        """'''+str(p)+'''"""
        </pre>
    '''
    msg = MIMEText(message,'html')

    msg['Subject'] = 'Verification'

    msg['To'] = em

    msg['From'] = 'onlinevotingbca@gmail.com'

    try:

        gmail.send_message(msg)

    except Exception as e:

        print("COULDN'T SEND EMAIL", str(e))

    return HttpResponse('<script>alert("accepted");window.location ="/candidateview/'+str(request.session['eid'])+'"</script>')


def rejectcan(request,id,em):
    candidates.objects.filter(id=id).update(status='rejected')
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)

        gmail.ehlo()

        gmail.starttls()

        gmail.login('onlinevotingbca@gmail.com', 'nkba zott ofxx rxad')

    except Exception as e:
        print("Couldn't setup email!!" + str(e))

    msg = MIMEText("Your candidate request rejected.")

    msg['Subject'] = 'Verification'

    msg['To'] = em

    msg['From'] = 'onlinevotingbca@gmail.com'

    try:

        gmail.send_message(msg)

    except Exception as e:

        print("COULDN'T SEND EMAIL", str(e))

    return HttpResponse('<script>alert("reject");window.location ="/candidateview/'+str(request.session['eid'])+'"</script>')
# =====coord

def view_coordinators(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "VIEW COORDINATOR"
    data = election_coordinator.objects.all()
    return render(request,"admin/view_coordinators.html",{"data":data})


def postview(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "POST"
    data = post.objects.all()
    return render(request,"admin/Post View.html",{"data":data})
def postdelete(request,id):
    post.objects.get(id = id).delete()
    return HttpResponse('<script>alert("deleted successfull");window.location ="/postview#home"</script>')


def postadd(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "ADD POST"
    return render(request,"admin/Post add.html")
def postaddpost(request):
    np = request.POST['textfield']
    de = request.POST['textarea']
    if post.objects.filter(post=np,details=de).exists():
        return HttpResponse('<script>alert("data already exists");window.location ="/postadd#home"</script>')
    pobj = post()
    pobj.post = np
    pobj.details = de
    pobj.save()
    return  HttpResponse('<script>alert("Added successfully");window.location ="/postadd#home"</script>')
def editpost(request,id):
    request.session['h'] = "EDIT POST"
    data = post.objects.get(id=id)
    return render(request,"admin/Edit Post.html",{"data":data})

def posteditpost(request,id):
    np = request.POST['textfield']
    de = request.POST['textarea']
    post.objects.filter(id=id).update(post=np, details=de,)
    return  HttpResponse('<script>alert("update successfull");window.location ="/postview#home"</script>')
def electionadd(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "ADD ELECTION"
    import datetime
    return render(request,"admin/Election.html",{"d":datetime.datetime.now().strftime("%Y-%m-%d")})
def electionpost(request):
    vd = request.POST['textfield']
    cam = request.POST['textfield2']
    ti = request.POST['textfield3']
    pd = request.POST['textfield4']
    ls = request.POST['textfield5']
    election.objects.all().update(status='completed')
    if election.objects.filter(votingdate=vd,campaign=cam,title=ti,publishingdate=pd,lastdatesubmission=ls).exists():
        return HttpResponse('<script>alert("data already exists");window.location ="/electionadd#home"</script>')
    pobj = election()
    pobj. votingdate = vd
    pobj.campaign = cam
    pobj.title = ti
    pobj.publishingdate = pd
    pobj.lastdatesubmission = ls
    pobj.save()
    return  HttpResponse('<script>alert("Added successfully");window.location ="/electionadd#home"</script>')
def electionedit(request,id):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "EDIT ELECTION"
    data = election.objects.get(id=id)
    return render(request,"admin/Election Edit.html",{"data":data})
def electioneditpost(request,id):
    vd = request.POST['textfield']
    cam = request.POST['textfield2']
    ti = request.POST['textfield3']
    pd = request.POST['textfield4']
    ld = request.POST['textfield5']
    election.objects.filter(id=id).update(votingdate=vd, campaign=cam,title=ti,publishingdate=pd,lastdatesubmission=ld)
    return   HttpResponse('<script>alert("update successfull");window.location ="/election1#home"</script>')
def election1(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "ELECTION"
    data=election.objects.filter(status='ongoing')
    return render(request,"admin/Election 1.html",{"data":data})

def admin_election(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "ELECTION"
    data=election.objects.filter(status='ongoing')
    return render(request,"admin/Election_admin.html",{"data":data})


def electiondelete(request,id):
    election.objects.get(id = id).delete()
    return HttpResponse('<script>alert("deleted successfull");window.location ="/election1#home"</script>')


def remove_coor(request,id):
    election_coordinator.objects.get(id = id).delete()
    return HttpResponse('<script>alert("deleted successfull");window.location ="/view_coordinators#home"</script>')



def complaint(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "COMPLAINTS"
    data = complaints.objects.all()
    return render(request,"admin/Complaint.html",{"data":data})

def changepswd(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "CHANGE PASSWORD"
    return render(request,"admin/Change password.html")
def changepswdpost(request):
    cp = request.POST['textfield']
    np = request.POST['textfield2']
    cnpb = request.POST['textfield3']
    if cp==np:
        return HttpResponse('<script>alert("password is same");window.location ="/changepswd#home"</script>')

    if login.objects.filter(password=cp,id =request.session['lid']).exists():
        if np == cnpb:
            login.objects.filter(usertype='admin',id=request.session['lid']).update(password=np)
            return HttpResponse('<script>alert("password created succesfully");window.location ="/"</script>')
        else:
            return HttpResponse('<script>alert("password incorrect");window.location ="/changepswd#home"</script>')
    else:
        return HttpResponse('<script>alert("password doesnot exist");window.location ="/changepswd#home"</script>')

def adminhome(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = ""
    return render(request,"admin/index.html")

def userinfo(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "REVIEW"
    data = review.objects.all()
    return render(request,"admin/user info.html",{"data":data})

def sendreplay(request,id):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "SEND REPLY"
    return render(request,"admin/send replay.html",{"id":id})
def sendreplaypost(request,id):
    rp = request.POST['r1']
    complaints.objects.filter(id=id).update(replay = rp)
    return HttpResponse('<script>alert("updated success fully");window.location ="/complaint#home"</script>')

def results(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "RESULTS"
    import datetime
    try:
        data2 = election.objects.get(Q(publishingdate=datetime.datetime.now().date()) | Q(
            publishingdate__lte=datetime.datetime.now().date()) & Q(status='ongoing'))
        data = result.objects.filter(CANDIDATE__ELECTION=data2.id).order_by('CANDIDATE__POST__id')
        return render(request, "admin/view result.html", {"data": data})
    except:
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')


def sendreason(request,id,em):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "SEND REASON"
    return render(request,"admin/Send reason.html",{"id":id,"em":em})
def sendreasonpost(request,id,em):
    rs = request.POST['textarea']
    candidates.objects.filter(id=id).update(status = 'Your application is rejected '+rs)
    # candidates.objects.filter(id=id).update(status='rejected')
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)

        gmail.ehlo()

        gmail.starttls()

        gmail.login('onlinevotingbca@gmail.com', 'nkba zott ofxx rxad')

    except Exception as e:
        print("Couldn't setup email!!" + str(e))

    msg = MIMEText("Your candidate request rejected."+rs)

    msg['Subject'] = 'Verification'

    msg['To'] = em

    msg['From'] = 'onlinevotingbca@gmail.com'

    try:

        gmail.send_message(msg)

    except Exception as e:

        print("COULDN'T SEND EMAIL", str(e))

    return HttpResponse('<script>alert("reject");window.location ="/candidateview/' + str(request.session['eid']) + '"</script>')

def logout(request):
    request.session['lin'] ="0"
    return HttpResponse('<script>alert("logout successfull ");window.location ="/"</script>')




#--------------------------------------------------------------------------------------------------------------------------


def addcampaign(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "ADD CAMPAIGN"
    return render(request,"candidates/add campaign.html")
def addcampaignpost(request):
    f = request.FILES['fileField']
    ft=f.name.split('.')
    if str(ft[-1]) == 'jpg':
        import datetime
        d = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        fs = FileSystemStorage()
        fs.save(r"C:\Users\Adarsh\OneDrive\Desktop\untitled\untitled\evoting\static\\" + d + '.'+str(ft[-1]), f)
        ds = request.POST['textarea']

        fobj = campaign()
        fobj.file='/static/'+d+'.'+str(ft[-1])
        fobj.description=ds
        fobj.type='image'
        fobj.date=datetime.datetime.now().date()
        fobj.CANDIDATE_id=request.session['cid']
        fobj.save()

    if str(ft[-1]) == 'png':
        import datetime
        d = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        fs = FileSystemStorage()
        fs.save(r"C:\Users\Adarsh\OneDrive\Desktop\untitled\untitled\evoting\static\\" + d + '.' + str(ft[-1]), f)
        ds = request.POST['textarea']

        fobj = campaign()
        fobj.file = '/static/' + d + '.' + str(ft[-1])
        fobj.description = ds
        fobj.type = 'image'
        fobj.date = datetime.datetime.now().date()
        fobj.CANDIDATE_id = request.session['cid']
        fobj.save()
    if str(ft[-1]) == 'mp4':
        import datetime
        d = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        fs = FileSystemStorage()
        fs.save(r"C:\Users\Adarsh\OneDrive\Desktop\untitled\untitled\evoting\static\\" + d + '.' + str(ft[-1]), f)
        ds = request.POST['textarea']

        fobj = campaign()
        fobj.file = '/static/' + d + '.' + str(ft[-1])
        fobj.description = ds
        fobj.type = 'vedio'
        fobj.date = datetime.datetime.now().date()
        fobj.CANDIDATE_id = request.session['cid']
        fobj.save()

    if str(ft[-1]) == 'mp3':
        import datetime
        d = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        fs = FileSystemStorage()
        fs.save(r"C:\Users\Adarsh\OneDrive\Desktop\untitled\untitled\evoting\static\\" + d + '.' + str(ft[-1]), f)
        ds = request.POST['textarea']

        fobj = campaign()
        fobj.file = '/static/' + d + '.' + str(ft[-1])
        fobj.description = ds
        fobj.type = 'audio'
        fobj.date = datetime.datetime.now().date()
        fobj.CANDIDATE_id = request.session['cid']
        fobj.save()

    return HttpResponse('<script>alert("Added successfully");window.location ="/addcampaign#home"</script>')


def candidatehome(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    return render(request,"candidates/index.html")
def viewcampaign(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    data = campaign.objects.filter(CANDIDATE=request.session['cid'])
    return render(request,"candidates/view campaign.html",{"data":data})

def viewcampaignothers(request,id):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    data = campaign.objects.filter(CANDIDATE_id=id)
    return render(request,"candidates/viewcampaignothers.html",{"data":data})

def campaigndelete(request,id):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    campaign.objects.get(id=id).delete()
    return HttpResponse('<script>alert("deleted successfull");window.location ="/viewcampaign#home"</script>')

def viewcandidates(request,id):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "CANDIDATES"
    request.session['eid'] = id
    data = candidates.objects.filter(POST=id)
    return render(request,"candidates/view candidate.html",{"data":data})


def viewpost(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "DESIGNATION"
    data = post.objects.all()
    return render(request,"candidates/view post.html",{"data":data})
def viewresult(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "RESULT"
    data = result.objects.all()
    return render(request,"candidates/view result.html",{"data":data})

def viewuser(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "STUDENT INFO"
    data = user.objects.all()
    return render(request,"candidates/view users.html",{"data":data})
def changepassword(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "CHANGE PASSWORD"
    return render(request,"candidates/change password.html")
def changepswdpost1(request):
    cp = request.POST['textfield']
    np = request.POST['textfield2']
    cnpb = request.POST['textfield3']
    if cp == np:
        return HttpResponse('<script>alert("password is same");window.location ="/changepswd#home"</script>')
    if login.objects.filter(password=cp,id=request.session['lid']).exists():
        if np == cnpb:
            login.objects.filter(usertype='candidates',id=request.session['lid']).update(password=np)
            return HttpResponse('<script>alert("password created succesfully");window.location ="/"</script>')
        else:
            return HttpResponse('<script>alert("password incorrect");window.location ="/changepswd1#home"</script>')
    else:
        return HttpResponse('<script>alert("password doesnot exist");window.location ="/changepswd1#home"</script>')

def logout1(request):
    request.session['lin'] = "0"
    return HttpResponse('<script>alert("logout successfull ");window.location ="/"</script>')


#------------------------------------------------------------------------------------------------

def changepassword1(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "CHANGE PASSWORD"
    return render(request,"students/Change password.html")
def changepswdpost2(request):
    cp = request.POST['textfield']
    np = request.POST['textfield2']
    cnpb = request.POST['textfield3']
    if cp == np:
        return HttpResponse('<script>alert("password is same");window.location ="/changepswd#home"</script>')
    if login.objects.filter(password=cp,id=request.session['lid']).exists():
        if np == cnpb:
            login.objects.filter(usertype='user',id=request.session['lid']).update(password=np)
            return HttpResponse('<script>alert("password created succesfully");window.location ="/"</script>')
        else:
            return HttpResponse('<script>alert("password incorrect");window.location ="/changepassword1#home"</script>')
    else:
        return HttpResponse('<script>alert("password doesnot exist");window.location ="/changepassword1#home"</script>')


def sendcomplaint(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "SEND COMPLAINT"
    return render(request, "students/Send complaint.html")

def sendcomplaintpost(request):
    sp = request.POST['textarea']
    cobj = complaints()
    cobj.comlaint=sp
    import datetime
    cobj.date= datetime.datetime.now().date()
    cobj.time= datetime.datetime.now().strftime("%H:%M:%S")

    cobj.USER_id = request.session['uid']
    cobj.replay='pending'
    cobj.save()
    return HttpResponse('<script>alert("Complaint send successfull");window.location ="/sendcomplaint#home"</script>')

def viewcomplaint(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "COMPLAINTS"
    data = complaints.objects.filter(USER_id = request.session['uid'])
    return render(request,"students/View complaint.html",{"data":data})

def sendreview(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "SEND REVIEW"
    return render(request,"students/Send review.html")

def sendreviewpost(request):
    sr = request.POST['textarea']
    robj = review()
    robj.USER_id = request.session['uid']
    robj.review = sr
    import datetime
    robj.date = datetime.datetime.now().date()
    robj.save()
    return HttpResponse('<script>alert("review send  successfull");window.location ="/sendreview#home"</script>')

def viewcampaign1(request,id):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "CAMPAIGNS"
    data = campaign.objects.filter(CANDIDATE_id=id)
    return render(request,"students/View campaign.html",{"data":data})

def viewcandidate1(request,id):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "CANDIDATE"
    data = post.objects.all()
    return render(request, "students/View candidate.html",{"data":data,"id":id})

def studenthome(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    return render(request,"students/index.html")

def viewcandidates1(request,id,eid):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "CANDIDATES"
    data = candidates.objects.filter(POST=id,ELECTION=eid)
    return render(request,"students/View candidates.html",{"data":data})

def viewelection(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "ELECTION"
    data = election.objects.filter(status='ongoing')
    return render(request,"students/View election.html",{"data":data})

def viewpost1(request,id):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "POST"
    e = election.objects.get(id=id)
    from datetime import datetime
    date_format = "%Y-%m-%d"
    a = datetime.strptime(str(datetime.now().date()), date_format)
    b = datetime.strptime(str(e.lastdatesubmission), date_format)
    delta = b - a
    d = (delta.days)
    print(d)
    if d >= 0 :
        data = post.objects.filter()
        return render(request,"students/View post.html",{"data":data,"id":id,"v":"1"})
    else:
        data = post.objects.filter()
        return render(request, "students/View post.html", {"data": data, "id": id,"v":"0"})

def viewresultmore(request,id,i):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "RESULTS"
    data = result.objects.filter(CANDIDATE__ELECTION=i,CANDIDATE__POST=id)
    print(data.count())
    if data.count() > 1:
        return render(request,"students/View result more.html",{"data":data})
    else:
        data2 = candidates.objects.filter(ELECTION=i, POST=id)
        print(data2,"jj")
        return render(request, "students/View result more.html", {"data2": data2[0]})


def viewresult1(request,id):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "RESULT"
    data = post.objects.all()
    return render(request,"students/View result.html",{"data":data,"id":id})

def viewrule1(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "RULES"
    data = rules.objects.all()
    return render(request, "students/View rule.html",{"data":data})

def applyascandidate(request,postid,eid):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "APPLY AS CANDIDATE"
    request.session['pppp'] = postid
    request.session['eeee'] = eid
    data = rules.objects.all()
    return render(request, "students/applyascandidate.html",{"data":data,"postid":postid,"eid":eid})



# ======================================================================

def voting(request):
    return render(request, "Voting.html")
def votingpost(request):
    e = request.POST['textfield']
    q = login.objects.filter(username=e,usertype='user')
    print(q)
    if q.exists():
        request.session['uid'] = user.objects.get(LOGIN=q[0].id).id
        request.session['sem'] = user.objects.get(LOGIN=q[0].id).sem

        request.session['crse'] = user.objects.get(LOGIN=q[0].id).course

        if vote.objects.filter(USER=request.session['uid'],CANDIDATE__ELECTION=request.session['eid']):
            return HttpResponse('<script>alert("Already voted");window.location ="/"</script>')


        p = random.randint(1111,9999)
        request.session['otp'] = p
        oobj = otp()
        oobj.USER_id = request.session['uid']
        oobj.otp =  p
        import datetime
        oobj.date = datetime.datetime.now().date()
        oobj.save()
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)

            gmail.ehlo()

            gmail.starttls()

            gmail.login('onlinevotingbca@gmail.com', 'nkba zott ofxx rxad')

        except Exception as e1:
            print("Couldn't setup email!!" + str(e1))

        msg = MIMEText("Your OTP is : " + str(p))

        msg['Subject'] = 'Verification'

        msg['To'] = e

        msg['From'] = 'onlinevotingbca@gmail.com'

        try:

            gmail.send_message(msg)

        except Exception as e1:

            print("COULDN'T SEND EMAIL", str(e1))

        return HttpResponse('<script>alert("Send successfull");window.location ="/otp#home"</script>')
    else:
        return HttpResponse('<script>alert("Email does not exist");window.location ="/"</script>')

def otp1(request):
    return render(request, "OTP.html")
def otppost(request):
    otp = request.POST['textfield']
    if str(request.session['otp'])== otp :
        request.session['pcount'] = 0
        return HttpResponse('<script>alert("Start your voting");window.location ="/votingpage#home"</script>')
    else:
        return HttpResponse('<script>alert("Invalid OTP");window.location ="/otp#home"</script>')


def forgo(request):
    return render(request, "forgot.html")



def forpost(request):
    un = request.POST['textfield']

    l = login.objects.filter(username=un)
    if l.exists():
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)

            gmail.ehlo()

            gmail.starttls()

            gmail.login('onlinevotingbca@gmail.com', 'nkba zott ofxx rxad')

        except Exception as e1:
            print("Couldn't setup email!!" + str(e1))

        msg = MIMEText("Your password is : " + str(l[0].password))

        msg['Subject'] = 'Verification'

        msg['To'] = un

        msg['From'] = 'onlinevotingbca@gmail.com'

        try:

            gmail.send_message(msg)

        except Exception as e1:

            print("COULDN'T SEND EMAIL", str(e1))

        return HttpResponse('<script>alert("Send successfull");window.location ="/#home"</script>')

    else:
        return HttpResponse('<script>alert("User does not exists");window.location ="/"</script>')



# ====================================================================


def coordinator_home(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')
    request.session['h']=""
    return render(request,"election_coordinator/index.html")

def evcomplaint(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "COMPLAINTS"
    data = complaints.objects.all()
    return render(request,"election_coordinator/vComplaint.html",{"data":data})

def coordreg(request):
    import datetime

    name=request.POST['n']
    phn=request.POST['ph']
    gnd=request.POST['g']
    em=request.POST['em']
    ps=request.POST['ps']
    f=request.FILES['file']
    d=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs=FileSystemStorage()
    fn=fs.save(f.name,f)
    # path="/static/"+d+'.jpg'
    if login.objects.filter(usertype="election_coordinator"):
        return HttpResponse('<script>alert("Please contact your admin !");window.location ="/"</script>')
    if login.objects.filter(username=em):
        return HttpResponse('<script>alert("Please contact your admin !");window.location ="/"</script>')

    obj1=login()
    obj1.username=em
    obj1.password=ps
    obj1.usertype="election_coordinator"
    obj1.save()
    obj=election_coordinator()
    obj.name=name
    obj.phno=phn
    obj.gender=gnd
    obj.email=em
    obj.photo=fn
    obj.LOGIN=obj1
    obj.save()


    return HttpResponse('<script>alert("Successfully Registered!");window.location ="/"</script>')


def candidateviewe(request,id):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "CANDIDATES"
    request.session['eid']=id
    data = candidates.objects.filter(Q(ELECTION=id)&( Q(status="pending") |  Q(status="approved")))
    return render(request,"election_coordinator/View reg candiates_forward.html",{"data":data})








def forward(request,id,em):
    q = candidates.objects.filter(id=id)
    q2=q.update(status = 'approved')
    p = random.randint(0000,9999)
    obj = login()
    obj.username = q[0].USER.email
    obj.password = p
    obj.usertype = 'candidate'
    obj.save()
    obj2 = candidatelogin()
    obj2.CANDIDATE_id=q[0].id
    obj2.LOGIN = obj
    obj2.save()

    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)

        gmail.ehlo()

        gmail.starttls()

        gmail.login('onlinevotingbca@gmail.com', 'nkba zott ofxx rxad')

    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    message ='''
        <pre>
        Your Candidate request accepted<br>
        Your password for candidate panel is  
        """'''+str(p)+'''"""
        </pre>
    '''
    msg = MIMEText(message,'html')

    msg['Subject'] = 'Verification'

    msg['To'] = em

    msg['From'] = 'onlinevotingbca@gmail.com'

    try:

        gmail.send_message(msg)

    except Exception as e:

        print("COULDN'T SEND EMAIL", str(e))

    return HttpResponse('<script>alert("accepted");window.location ="/election1"</script>')



def allvoteduser(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')
    import datetime
    request.session['h'] = "VOTER'S LIST"
    data = vote.objects.filter(CANDIDATE__ELECTION=election.objects.get(publishingdate=datetime.datetime.now().date()).id)
    return render(request,"election_coordinator/User view.html",{"data":data})



def eresults(request):
    if request.session['lin'] == "0":
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')

    request.session['h'] = "RESULTS"
    import datetime
    try:
        data2 = election.objects.get(Q(publishingdate=datetime.datetime.now().date()) | Q(
            publishingdate__lte=datetime.datetime.now().date()) & Q(status='ongoing'))
        data = result.objects.filter(CANDIDATE__ELECTION=data2.id).order_by('CANDIDATE__POST__id')
        return render(request, "election_coordinator/view result.html", {"data": data})
    except:
        return HttpResponse('<script>alert("Your session has expired");window.location ="/"</script>')



# ======================================================================================================================

def and_login(request):
    username = request.POST['uname']
    password = request.POST['pswd']
    import datetime
    try:
        # e = election.objects.filter(publishingdate__gt=datetime.datetime.now().date())
        # if e.exists():
        #     return JsonResponse({"task": "Invalid"})
        ob = login.objects.get(username=username, password=password)
        print(ob)

        if ob is None:
            print("oooooooooooooooooooooooooooooooooooooooooo")
            return JsonResponse({"task": "invalid"})

        else:
            print("-----------------------------------")
            import datetime
            e = election.objects.filter(votingdate=datetime.datetime.now().date())
            if e.exists():
                print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
                if vote.objects.filter(CANDIDATE__ELECTION=e[0], USER__LOGIN=ob).exists():
                    print("+++++++++++++++++++++++++++++++++++++++++")
                    print(ob.id,ob.usertype)
                    print("+++++++++++++++++++++++++++++++++++++++++")
                    return JsonResponse({"task": "valid", "lid": ob.id, "type": ob.usertype, "es": "0"})
                else:
                    print("***************************************************")
                    print(ob.id,ob.usertype)
                    print("***************************************************")
                    return JsonResponse({"task": "valid", "lid": ob.id,"type":ob.usertype,"es":"1"})
            else:
                print("///////////////////////////////////////")
                print(ob.id,ob.usertype)
                print("///////////////////////////////////////")
                return JsonResponse({"task": "valid", "lid": ob.id,"type":ob.usertype,"es":"0"})
    except Exception as e:
        print("ki",e)
        return JsonResponse({"task": "Invalid"})
def and_complaint(request):
    import datetime
    o = complaints()
    o.comlaint = request.POST['dyc']
    o.USER = user.objects.get(LOGIN=request.POST['lid'])
    o.replay = 'pending'
    o.date = datetime.datetime.now().strftime("%Y-%m-%d")
    o.time = datetime.datetime.now().strftime("%H:%M")
    o.save()
    return JsonResponse({"status": "ok"})

def and_view_reply(request):
    o = complaints.objects.filter(USER__LOGIN=request.POST['lid'])
    data = []
    for i in o:
        data.append({
            "cid":i.id,
            "Complaint":i.comlaint,
            "Date":i.date +'   '+ i.time,
            "reply":i.replay,
        })

    return JsonResponse({"status": "ok","data":data})



def and_post(request):
    o = post.objects.filter()
    print("ooo",o)
    data = []
    for i in o:
        data.append({
            "pid":i.id,
            "p":i.post,
            "d": i.details,

        })

    return JsonResponse({"status": "ok","data":data})

def and_rule(request):
    o = rules.objects.filter()
    print("ooo",o)
    data = []
    for i in o:
        data.append({
            "pid":i.id,
            "p":i.title + str(":") +i.description,


        })

    return JsonResponse({"status": "ok","data":data})


def and_election(request):
    try:
        data = election.objects.get(status='ongoing')
        return JsonResponse({"task": "valid","t":data.title,"e":data.votingdate,"n":data.lastdatesubmission,"c":data.campaign,"r":data.publishingdate})
    except:
        return JsonResponse({"task": "no"})

def applyascandidatepost(request):
    f = request.FILES['pic']
    d2 = request.POST['d']
    e = request.POST['s1']
    ee = request.POST['s2']
    print( user.objects.get(email=e).id)
    print( user.objects.get(email=ee).id)
    eid = election.objects.filter(status='ongoing')
    if user.objects.filter(email=e).exists()  and user.objects.filter(email=ee).exists():
        import datetime
        d = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        fs = FileSystemStorage()
        fs.save(r"C:\Users\Adarsh\OneDrive\Desktop\untitled\untitled\evoting\static\\" + d + '.png', f)
        if candidates.objects.filter(USER=user.objects.get(LOGIN=request.POST['lid']), ELECTION_id=eid[0]):
            return JsonResponse({"status":"no"})
        print(eid)
        cobj = candidates()
        cobj.USER_id =user.objects.get(LOGIN= request.POST['lid']).id
        cobj.POST_id = request.POST['pid']
        cobj.ELECTION_id = eid[0].id
        cobj.details = d2
        # cobj.CCANDIDATE1_id =2
        cobj.CCANDIDATE1_id = user.objects.get(email=e).id
        cobj.CCANDIDATE2_id = user.objects.get(email=ee).id
        # cobj.CCANDIDATE2_id = 4
        cobj.Document = '/static/' + d + '.png'
        cobj.status = 'pending'
        cobj.save()
        return JsonResponse({"status":"ok"})
    else:
        return JsonResponse({"status": "Invalid Email"})



def and_view_nominees(request):
    o = candidates.objects.filter(ELECTION=election.objects.get(status='ongoing'),POST=request.POST['lid'])
    data = []
    for i in o:
        data.append({
            "cid":i.id,
            "Complaint":i.USER.name,
            "Date":i.USER.photo,
            "reply":i.USER.COURSE.coursename,
        })

    return JsonResponse({"status": "ok","data":data})

def and_verification(request):
    oo = candidates.objects.filter(ELECTION=election.objects.get(status='ongoing'))
    if oo.exists():
        o = o = candidates.objects.filter(USER__LOGIN=request.POST['lid'],ELECTION=election.objects.get(status='ongoing'))
        print(o,"00000",request.POST['lid'])
        if o.exists():
            return JsonResponse({"task": "valid","t":"Your application for " + str(o[0].POST.post) + " is " + str(o[0].status) })
        else:
            return JsonResponse(
                {"task": "no", "t": "You have no application for " + str(oo[0].ELECTION.title)})
    else:
        print("0000")
        return JsonResponse(
            {"task": "no", "t": "You have no application for " +str(oo[0].ELECTION.title)})



def uviewresult(request):
    import datetime
    data_new = []
    data = election.objects.filter(publishingdate__lte =  datetime.datetime.now().strftime("%Y-%m-%d"),status='ongoing').order_by('-id')
    if data.exists():
        d = post.objects.all()
        for post_object in d:
            data3 = candidates.objects.filter(POST=post_object.id, status='approved', ELECTION=data[0].id)
            if len(data3) == 1:
                data_new.append({
                     data_new.append({
                    "cid": post_object.post,
                    "Complaint" : data3[0].USER.name + "(" + 'Single Candidate' + ")",
                    "Date":   data3[0].USER.photo,
                         "s":''
                })
                # post_object.s = ''
                # post_object.candi = candidate.photo
                # post_object.candin = candidate.name
                })
            else:
                print(post_object.post)

                data2 = result.objects.filter(CANDIDATE__ELECTION=data[0].id, CANDIDATE__POST=post_object.id,
                                              CANDIDATE__status='approved')
                if data2.exists():
                    v = []
                    c = []
                    for i in data2:
                        v.append(i.result)
                        c.append(i.CANDIDATE.id)

                    aindex = c[v.index(max(v))]

                    candidate = candidates.objects.get(id=aindex).USER
                    # post_object.count = k['max_result']
                    # post_object.s = k['max_result']
                    # post_object.candi = candidate.photo
                    # post_object.candin = candidate.name

                    data_new.append({
                        "cid": post_object.post,
                        "Complaint": candidate.name + "(" + str(max(v)) + ")",
                        "Date":candidate.photo,
                        "s":  max(v)
                    })
                else:
                    # post_object.count = ''
                    # post_object.s = 'aaa'
                    # post_object.candi = '/static/s.png'
                    # post_object.candin = 'No Candidates'

                    data_new.append({
                        "cid": post_object.post,
                        "Complaint": 'No Candidates',
                        "Date": '/static/s.png',
                        "s": 'aaa'
                    })



        # for i in d:
        #     print(i.count)
        # print(data_new,"ji")
        return JsonResponse({"data":data_new,"status":"ok"})
    else:
        return JsonResponse({"status":"Please Wait For publish result"})



def votingpage(request):

    try:
        import datetime
        p = post.objects.all()[int(request.POST['pcount'])]
        print(p,"ppp")
        e = election.objects.get(votingdate=datetime.datetime.now().date(),status='ongoing')
        c = candidates.objects.filter(ELECTION=e.id, status='approved', POST=p)
        if c.count() == 1:
            return JsonResponse({"status": "Only One nomination"})
        if c.count() == 0:
            return JsonResponse({"status": "No candidates"})

        else:
            data = []
            c = candidates.objects.filter(ELECTION=e.id, status='approved', POST=p)
            for i in c:
                data.append({
                    "cid": i.id,
                    "Complaint":i.USER.name,
                    "Date" : i.USER.photo,
                    "reply":i.details
                })
            return JsonResponse({"status":"ok","data":data,"p":p.post})


    except Exception as e:
        print(e,"er")
        return JsonResponse({"status":"Voting Completed"})

def votes(request):
    import datetime
    v = vote()
    v.USER_id = user.objects.get(LOGIN=request.POST['lid']).id
    v.CANDIDATE = candidates.objects.get(id = request.POST['cid'])
    v.date = datetime.datetime.now().date()
    v.time = datetime.datetime.now().strftime("%H:%M")
    v.save()
    r2 = result.objects.filter(CANDIDATE_id =request.POST['cid'])
    if r2.exists():
        r24 = int(r2[0].result)+1
        r2.update(result=r24)
    else:
        r = result()
        r.CANDIDATE_id =request.POST['cid']
        r.result = 1
        r.save()
    return  JsonResponse({"status":"ok"})




def addimg(request):
    try:
        print(request.POST,"====================================================")
        img=request.FILES['files']
        lid=request.POST['lid']
        print(lid,img,"=======================")
        fnn=FileSystemStorage()
        import time
        # fn=time.strftime("%Y%m%d_%H%M%S")+".jpg"
        fnn.save(r"C:\Users\hazna\Documents\ekc\untitled\untitled\evoting\static/"+img.name,img)
        s=user.objects.filter(LOGIN__id=lid)
        print(s,"===================")
        res1=enf(r"C:\Users\hazna\Documents\ekc\untitled\untitled\evoting\static/"+img.name)
        print(res1,"**************")
        for r in s:
            res=rec_face_image(r"C:\Users\hazna\Documents\ekc\untitled\untitled\evoting\static/"+str(r.photo))
            if len(res)>0:
                name=str(r.fname)+" "+str(r.lname)
                print(name,"===================")
                # idd=r.login.id
                return JsonResponse({"result":"yes"})
            else:
                return JsonResponse({"result": "na" })
    except:
        return JsonResponse({"result": "na" })




