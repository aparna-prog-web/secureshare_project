import os
import smtplib
from datetime import  datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tokenize import Comment
from PIL import Image

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.checks import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import face_recognition


# Create your views here.
from myapp.models import *

@login_required(login_url='/myapp/login_get/')
def adminhome(request):
    return render(request,"adminindex.html")

def login_get(request):
    return render(request,"login.html")

def login_post(request):
    username=request.POST["username"]
    password=request.POST["password"]
    user=authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user)
        if user.groups.filter(name="admin"):
            return redirect('/myapp/adminhome/')
        else:
            return redirect('/myapp/login_get/')
    else:
        return redirect('/myapp/login_get/')

@login_required(login_url='/myapp/login_get/')
def change_password(request):
    return render(request,"changepassword.html")

@login_required(login_url='/myapp/login_get/')
def change_password_post(request):
    current_password=request.POST['current password']
    new_password=request.POST['new password']
    confirm_password=request.POST['confirm password']
    user = request.user
    if  user.check_password(current_password):
        if new_password==confirm_password:
            user.set_password(new_password)
            user.save()
            return redirect('/myapp/login_get/')
        else:
            return redirect('/myapp/change_password/')
    else:
        return redirect('/myapp/change_password/')

@login_required(login_url='/myapp/login_get/')
def view_review(request):
    data=Review.objects.all()
    return render(request,"view review.html",{'data':data})


@login_required(login_url='/myapp/login_get/')
def send_reply(request,id):
    request.session['rid']=id
    return render(request,"sentreply.html")

@login_required(login_url='/myapp/login_get/')
def sent_reply_post(request):
    Reply=request.POST['Reply']
    Complaints.objects.filter(id=request.session['rid']).update(reply=Reply,status="replied")
    return redirect('/myapp/view_complaint/')


@login_required(login_url='/myapp/login_get/')
def view_complaint(request):
    data = Complaints.objects.all()
    return render(request,"viewcomplaint.html",{'data':data})

@login_required(login_url='/myapp/login_get/')
def view_user(request):
    data = Customer.objects.all()
    return render(request,"viewuser.html",{'data':data})


@login_required(login_url='/myapp/login_get/')
def addeducationalcontent_get(request):
    return render(request,'addeducationcontent.html')

@login_required(login_url='/myapp/login_get/')
def addeducationalcontent_post(request):
    content = request.FILES['content']
    ext = os.path.splitext(content.name)[1].lower()

    if ext == '.mp4':
        content_type = 'video'
    else:
        content_type = 'image'

    fs = FileSystemStorage()
    date = datetime.now().strftime('%Y%m%d%H%M%S') + ext
    fs.save(date, content)
    path = fs.url(date)

    a = EducationalContents()
    a.date = datetime.now().date()
    a.time = datetime.now().time()
    a.type = content_type
    a.content = path
    a.save()
    return redirect('/myapp/vieweducationalcontent_get/#abc')

@login_required(login_url='/myapp/login_get/')
def editeducationalcontent_get(request,id):
    a=EducationalContents.objects.get(id=id)
    return render(request,'editeducationcontent.html',{'data':a})

@login_required(login_url='/myapp/login_get/')
def editeducationalcontent_post(request):
    id = request.POST['id']

    a = EducationalContents.objects.get(id=id)

    if 'content' in request.FILES:
        content = request.FILES['content']
        ext = os.path.splitext(content.name)[1].lower()

        if ext == '.mp4':
            content_type = 'video'
        else:
            content_type = 'image'

        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d%H%M%S') + ext
        fs.save(date, content)
        path = fs.url(date)
        a.content = path
        a.type = content_type

        a.save()

    a.date = datetime.now().date()
    a.time = datetime.now().time()
    a.save()
    return redirect('/myapp/vieweducationalcontent_get/#abc')

@login_required(login_url='/myapp/login_get/')
def vieweducationalcontent_get(request):
    a=EducationalContents.objects.all()
    return render(request,'vieweducationalcontent.html',{'data':a})


@login_required(login_url='/myapp/login_get/')
def deleteeducationalcontent_get(request,id):
    EducationalContents.objects.get(id=id).delete()
    return redirect('/myapp/vieweducationalcontent_get/#abc')



def forgetpassword_get(req):
    return render(req,'forgetpassword.html')


def forgetpassword_post(req):
    if req.method == 'POST':
        email = req.POST.get('forget','').strip()
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(req,'Email does not exist')
            return redirect('/myapp/login_get/')
        import random
        psw = random.randint(1000,9999)

        user.set_password(str(psw))
        user.save()

        try:
            server=smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('trainingstarted@gmail.com', 'nlxasujxgazlbmgz')

            subject = "Password Reset - Construction App"
            body = "Your new password is: "+str(psw)
            msg = f"Subject: {subject}\n\n{body}"

            server.sendmail("trainingstarted@gmail.com",email, msg)
            server.quit()

            messages.success(req,'Password reset Successfuly. Please check your mail for new password')
            return  redirect('/myapp/login_get/')
        except Exception as e:
            messages.warning(req,'Faild to reset password')
            return  redirect('/myapp/login_get_web/')


    messages.warning(req,'Faild to reset password')
    return redirect('/myapp/login_get')



def logout_get(request):
    logout(request)
    return redirect('/myapp/login_get/')


#
# def login_post(request):
#     username = request.POST["username"]
#     password = request.POST["password"]
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         if user.groups.filter(name="admin"):
#             return redirect('/myapp/adminhome/')
#         else:
#             return redirect('/myapp/login_get/')
#     else:
#         return redirect('/myapp/login_get/')
#



def user_signup_post(request):
    name=request.POST['uname']
    photo=request.FILES['photo']
    profilephoto=request.FILES['profilephoto']
    email=request.POST['uemail']
    phone=request.POST['uphoneno']
    gender=request.POST['ugender']
    dob=request.POST['udob']
    place=request.POST['uplace']
    bio=request.POST['ubio']
    password=request.POST['upassword']
    confirm_password=request.POST['uconfirm_password']

    print(password,'--')


    if password!=confirm_password:
        return JsonResponse({'status':'password do not match'})

    if User.objects.filter(username=email):
        return JsonResponse({'status': 'email'})

    if Customer.objects.filter(phone=phone):
        return JsonResponse({'status': 'phone'})

    a=User.objects.create_user(username=email,password=password)
    a.groups.add(Group.objects.get(name='user'))
    a.save()


    fs=FileSystemStorage()
    date=datetime.now().strftime('%Y%m%d-%H%M%S')+'.jpg'
    fs.save(date,photo)
    from PIL import Image, ImageOps

    filepath = "C:\\Kmct\\web\\secureshare\\media\\" + date

    # Fix orientation using EXIF
    image = Image.open(filepath)
    image = ImageOps.exif_transpose(image)

    # Save corrected image
    image.save(filepath)

    path=fs.url(date)

    fs1 = FileSystemStorage()
    date1 = datetime.now().strftime('%Y%m%d-%H%M%S') + '_profile.jpg'
    fs1.save(date1, profilephoto)
    path1 = fs.url(date1)

    obj=Customer()
    obj.name=name
    obj.photo=path
    obj.profilephoto=path1
    obj.email=email
    obj.phone=phone
    obj.gender=gender
    obj.dob=dob
    obj.place=place
    obj.bio=bio
    obj.USER=a
    obj.save()
    return JsonResponse({'status': 'ok'})

def user_login_post(request):
    username=request.POST['Username']
    password=request.POST['Password']

    check=authenticate(request,username=username,password=password)
    if check is  not None:

        if check.groups.filter(name='user').exists():
             return JsonResponse({'status':'ok','lid':(check.id)})
        else:
            return JsonResponse({'status':'no'})
    else:
        return JsonResponse({'status':'no'})
#
# def user_view_profile(request):
#     lid=request.POST['lid']
#     data=Customer.objects.get(USER=lid)
#     data1=Post.objects.filter(CUSTOMER__USER_id=lid).count()
#     data2=Request.objects.filter(Tor_id=lid,status = 'pending').count()
#     data3=Request.objects.filter(Tor_id=lid,status = 'accepted').count()
#     data4=Request.objects.filter(Fromr_id=lid,status = 'accepted').count()
#     t=data3+data4
#     return JsonResponse({
#         'status':'ok',
#         'name':data.name,
#         'photo':data.profilephoto,
#         'email':data.email,
#         'phone':data.phone,
#         'gender':data.gender,
#         'dob': data.dob,
#         'place':data.place,
#         'bio':data.bio,
#         'post':data1,
#         'frnds':data2,
#         'frndss':t,
#     })
#
#
from django.http import JsonResponse
from django.db.models import Q

def user_view_profile(request):
    lid = request.POST['lid']

    data = Customer.objects.get(USER_id=lid)

    post_count = Post.objects.filter(
        CUSTOMER__USER_id=lid
    ).count()

    # Followers → people following me
    followers_count = Request.objects.filter(
        Tor_id=lid,
        status='accepted'
    ).count()

    # Following → people I follow
    following_count = Request.objects.filter(
        Fromr_id=lid,
        status='accepted'
    ).count()

    return JsonResponse({
        'status': 'ok',
        'name': data.name,
        'photo': data.profilephoto,
        'email': data.email,
        'phone': data.phone,
        'gender': data.gender,
        'dob': data.dob,
        'place': data.place,
        'bio': data.bio,
        'post': post_count,
        'followers': followers_count,
        'following': following_count,
    })


def viewusers(request):
    lid=request.POST['lid']
    a=Customer.objects.all().exclude(USER_id=lid)
    l=[]
    for i in a:
        l.append({'name': i.name,
                  'photo': i.profilephoto,
                  'email': i.email,
                  'phone': i.phone,
                  'gender': i.gender,
                  'dob': i.dob,
                  'place': i.place,
                  'bio': i.bio,
                  'id': i.id,
                  'u_id': i.USER.id,
                  })
    return JsonResponse({'status':'ok','data':l})


def sendrequest(request):
    lid=request.POST['lid']
    uid=request.POST['uid']
    print(lid,uid)
    from datetime import datetime
    r=Request()
    r.date=datetime.now().today()
    r.status='request'
    r.Fromr=User.objects.get(id=lid)
    r.Tor=User.objects.get(id=uid)
    r.save()
    return JsonResponse({'status': 'ok'})

#
# def userview_allrequest(request):
#     lid=request.POST['lid']
#     print(lid,'sjdsb')
#     requests = Request.objects.filter(Fromr_id=lid)
#
#     data = []
#     for i in requests:
#         data.append({
#             'id': i.id,
#             'user': i.Tor.username,
#             'date': i.date,
#             'status': i.status,
#             'userid': i.USER.id,
#         })
#
#     return JsonResponse({'status': 'ok', 'data': data})
#
#
# def userview_requeststatus(request):
#     lid = request.POST['lid']
#
#     requests = Request.objects.filter(Tor_id=lid)
#
#     data = []
#     for i in requests:
#         u=Customer.objects.get(USER_id=i.Fromr)
#         data.append({
#
#             'id': i.id,
#             'user': u.name,
#             'photo':u.photo,
#             'date': i.date,
#             'status': i.status,
#             'userid': u.USER.id,
#         })
#     print(data,"lllll")
#     return JsonResponse({'status': 'ok', 'data': data})








def userview_allrequest(request):
    lid = request.POST['lid']
    print(lid, 'sender id')

    # Requests SENT by this user
    requests = Request.objects.filter(Fromr_id=lid)

    data = []
    for i in requests:
        # i.Tor is a User object
        to_user = i.Tor

        # get Customer linked to TO user
        u = Customer.objects.get(USER=to_user)

        data.append({
            'id': i.id,
            'user': u.name,              # receiver name
            'date': i.date,
            'status': i.status,
            'userid': to_user.id,
        })

    return JsonResponse({'status': 'ok', 'data': data})



def userview_requeststatus(request):
    lid = request.POST['lid']

    requests = Request.objects.filter(Tor_id=lid)

    data = []
    for i in requests:
        u=Customer.objects.get(USER_id=i.Fromr)
        data.append({

            'id': i.id,
            'user': u.name,
            'photo':u.photo,
            'date': i.date,
            'status': i.status,
            'userid': u.USER.id,
        })
    print(data,"lllll")
    return JsonResponse({'status': 'ok', 'data': data})



def usereditprofile(request):
    id=request.POST['lid']
    name = request.POST['uname']
    email = request.POST['uemail']
    phone = request.POST['uphoneno']
    gender = request.POST['ugender']
    dob = request.POST['udob']
    place = request.POST['uplace']
    bio = request.POST['ubio']
    obj = Customer.objects.get(USER_id=id)

    if 'profilephoto' in request.FILES:
        photo = request.FILES['profilephoto']
        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
        fs.save(date, photo)
        path = fs.url(date)
        obj.profilephoto = path
        obj.save()

    obj.name = name
    obj.email = email
    obj.phone = phone
    obj.gender = gender
    obj.dob = dob
    obj.place = place
    obj.bio = bio
    obj.save()
    return JsonResponse({'status': 'ok'})


def userchangepassword(request):
    id = request.POST['lid']
    currentpassword = request.POST['currentpassword']
    newpassword = request.POST['newpassword']
    confirmpassword = request.POST['confirmpassword']

    a=User.objects.get(id=id)
    if a.check_password(currentpassword):
        if newpassword==confirmpassword:
            a.set_password(newpassword)
            a.save()
            logout(request)
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'no'})
    else:
        return JsonResponse({'status': 'no'})

# a=User.objects.get(username='sarunjith@gmail.com')
# a.set_password('12345')
# a.save()

def add_post(request):
    file=request.FILES['image']
    description=request.POST['description']
    caption=request.POST['caption']
    place=request.POST['place']
    id=request.POST['lid']
    from datetime import datetime




    ###############################algorithm codes
    fs = FileSystemStorage()
    date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.png'
    fs.save(date, file)
    from PIL import Image, ImageOps

    filepath = "C:\\Kmct\\web\\secureshare\\media\\" + date

    # Fix orientation using EXIF
    image = Image.open(filepath)
    image = ImageOps.exif_transpose(image)

    # Save corrected image
    image.save(filepath)

    path = fs.url(date)
    # path = fs.url(date)



    from transformers import CLIPProcessor, CLIPModel
    from PIL import Image
    import torch

    model_id = "openai/clip-vit-large-patch14"
    model = CLIPModel.from_pretrained(model_id)
    processor = CLIPProcessor.from_pretrained(model_id)

    labels = [
        "middle finger gesture",
        "obscene gesture",
        "rude gesture",
        "vulgar pose",
        "offensive sign",
        "abusive behaviour",
        "sexually explicit image",
        "graphic content",
        "safe image"
    ]

    def clip_vulgarity_score(path):
        image = Image.open(path).convert("RGB")
        inputs = processor(
            text=labels,
            images=image,
            return_tensors="pt",
            padding=True
        )
        with torch.no_grad():
            outputs = model(**inputs)
        logits = outputs.logits_per_image[0]
        probs = torch.softmax(logits, dim=0)

        return dict(zip(labels, probs.tolist()))

    is_vulg=False
    a=clip_vulgarity_score("C:\\Kmct\\web\\secureshare\\media\\" + date)
    pass#(a)

    la=""
    for label, score in a.items():
        print(f"{label}: {score:.4f}")

        if score>0.2:
            print("Vulgar content detected due to:", label)
            la = f"{label}: {score:.4f}"
            is_vulg=True

        if label == "safe image" and score>0.1:
            is_vulg=False
            break


    if is_vulg:
        return JsonResponse({'status': 'exp','vulg': la})


    from datetime import datetime
    # date = datetime.now().strftime('%Y-%m-%d')
    obj=Post()
    obj.file=path

    obj.date=datetime.now().today()
    obj.caption=caption
    obj.description=description
    obj.place=place
    obj.CUSTOMER=Customer.objects.get(USER_id=id)
    obj.save()


    u = Customer.objects.all().exclude(USER_id=id)
    uids = []
    imgs = []

    import face_recognition

    mediapth = "C:\\Kmct\\web\\secureshare\\media\\"

    for i in u:
        try:
            picture_of_me = face_recognition.load_image_file(mediapth + i.photo.replace("/media/", ""))
            my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

            imgs.append(my_face_encoding)
            uids.append(i.id)  # ← MOVE HERE

            print("Encoding successful for user id", i.id)

        except Exception as e:
            print("Error processing image for user id", i.id, ":", e)
            pass

    unknownfacesimages = "C:\\Kmct\\web\\secureshare\\media\\" + date

    picture_of_me = face_recognition.load_image_file(unknownfacesimages)
    my_face_encoding = face_recognition.face_encodings(picture_of_me)
    import  numpy as np

    from ultralytics import YOLO
    from PIL import Image
    image = Image.open(unknownfacesimages).convert("RGB")
    rgb_img = np.array(image)
    face_locations = face_recognition.face_locations(rgb_img)

    import cv2
    img = face_recognition.load_image_file(unknownfacesimages)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(img_rgb)

    unknownfacesimages = "C:\\Kmct\\web\\secureshare\\media\\" + date

    from PIL import Image
    # Open an image
    imagenews = Image.open(unknownfacesimages)
    # width, height = imagenews.size
    # results = model(img)

    # Load YOLO person model
    person_model = YOLO("yolov8m.pt")

    results = person_model(img)

    face_count = 0
    already_notified = set()

    def modify_pixel(pixel):
        return (pixel[0] ^ 124, pixel[1] ^ 178, pixel[2] ^ 167)

    # ----------------------------
    # PERSON → FACE → MATCH
    # ----------------------------
    for result in results:
        for box in result.boxes:

            cls = int(box.cls[0])

            # class 0 = person
            if cls != 0:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            person_crop = img[y1:y2, x1:x2]

            # Detect face inside person
            rgb_crop = cv2.cvtColor(person_crop, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_crop)
            face_encodings = face_recognition.face_encodings(rgb_crop, face_locations)

            for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):

                # Convert to global coordinates
                top_global = y1 + top
                bottom_global = y1 + bottom
                left_global = x1 + left
                right_global = x1 + right

                face_count += 1

                # Match with known users
                if len(imgs) == 0:
                    continue

                s = face_recognition.compare_faces(imgs, face_encoding, tolerance=0.58)
                print(s,'hh')

                for idx in range(len(s)):
                    print(s[idx])
                    if s[idx] == True:

                        matched_user_id = uids[idx]
                        print(matched_user_id,'hellloooo')

                        if matched_user_id in already_notified:
                            continue

                        already_notified.add(matched_user_id)

                        print("Matched:", matched_user_id)

                        p = PostNotification()
                        p.POST = obj
                        p.USER_id = matched_user_id
                        p.status = "pending"
                        p.date = datetime.now().date()
                        p.bottom = bottom_global
                        p.left = left_global
                        p.right = right_global
                        p.top = top_global
                        p.save()

                        # # ---- KEEP YOUR ORIGINAL BLUR ----
                        for x in range(left_global, right_global):
                            for y in range(top_global, bottom_global):
                                pixel = imagenews.getpixel((x, y))
                                new_pixel = modify_pixel(pixel)
                                imagenews.putpixel((x, y), new_pixel)

    print("Total faces detected:", face_count)

    imagenews.save(unknownfacesimages)






    print(imagenews)
    return JsonResponse({'status':'ok'})

def view_post(request):
    id=request.POST['lid']
    a=Post.objects.filter(CUSTOMER__USER_id=id)
    l=[]
    for i in a:
        l.append({
            'file':i.file,
            'date':i.date,
            'type':i.type,
            'caption':i.caption,
            'longitude':i.longitude,
            'latitude':i.latitude,

        })
    return JsonResponse({'status': 'ok', 'data': l})


def accept_request(request):
    id=request.POST['id']
    Request.objects.filter(id=id).update(status='accepted')
    return JsonResponse({'status': 'ok'})



def reject_request(request):
    id=request.POST['id']
    Request.objects.filter(id=id).update(status='rejected')
    return JsonResponse({'status': 'ok'})

#
# def userview_requeststatus(request):
#     lid = request.POST['lid']
#
#     requests = Request.objects.filter(Tor_id=lid)
#
#     data = []
#     for i in requests:
#         data.append({
#             'id': i.id,
#             'user': i.Tor.username,
#             'date': i.date,
#             'status': i.status,
#             'userid':i.Tor.id,
#         })
#
#     return JsonResponse({'status': 'ok', 'data': data})
#
# def userview_requeststatus(request):
#     lid = request.POST['lid']
#
#     requests = Request.objects.filter(Tor_id=lid)
#
#     data = []
#     for i in requests:
#         u=Customer.objects.get(USER_id=i.Fromr)
#         data.append({
#
#             'id': i.id,
#             'user': u.name,
#             'photo':u.photo,
#             'date': i.date,
#             'status': i.status,
#             'userid': u.USER.id,
#         })
#     print(data,"lllll")
#     return JsonResponse({'status': 'ok', 'data': data})
#



def view_friendprofile(request):
    id = request.POST['id']
    a=Customer.objects.get(USER_id=id)

    return JsonResponse({
        'status':'ok',
        'name':a.name,
        'photo':a.photo,
        'email':a.email,
        'phone':a.phone,
        'gender':a.gender,
        'dob':a.dob,
        'place':a.place,
        'bio':a.bio,
    })


def add_add_post(request):
    file=request.FILES['photo']
    description=request.POST['description']
    caption=request.POST['caption']
    place=request.POST['place']
    id=request.POST['lid']

    fs = FileSystemStorage()
    date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
    fs.save(date, file)
    path = fs.url(date)

    obj=Post()
    obj.date=datetime.now().today()
    obj.file=path
    obj.description=description
    obj.caption=caption
    obj.place=place
    obj.like=0
    obj.CUSTOMER=Customer.objects.get(USER_id=id)
    obj.save()
    return JsonResponse({'status':'ok'})



def userviewmy_post(request):
    id=request.POST['lid']
    a=Post.objects.filter(CUSTOMER__USER_id=id)
    l=[]
    for i in a:
        likes = 0
        if Likes.objects.filter(POST=i.id).exists():
            likes = Likes.objects.filter(POST=i.id).count()
        l.append({
            'id':i.id,
            'file':i.file,
            'date':i.date,
            'description':i.description,
            'caption':i.caption,
            'place':i.place,
            'like':likes,
        })
    return JsonResponse({'status':'ok','data':l})





def userviewmy_notifications(request):
    id=request.POST['lid']
    a=PostNotification.objects.filter(USER__USER_id=id,status='pending')
    l=[]
    for i in a:
        l.append({
            'id':i.id,
            'file':i.POST.file,
            'date':i.POST.date,
            'description':i.POST.description,
            'caption':i.POST.caption,
            'place':i.POST.place,
            'like':i.POST.like,
            'name':i.POST.CUSTOMER.name,
            'photo':i.POST.CUSTOMER.photo,

        })
    return JsonResponse({'status':'ok','data':l})


def user_deletepost(request):
    id=request.POST['id']
    Post.objects.get(id=id).delete()
    return JsonResponse({'status':'ok'})


def user_deletecomment(request):
    id=request.POST['id']
    Comments.objects.get(id=id).delete()
    return JsonResponse({'status':'ok'})

# import random
# from django.http import JsonResponse
#
# def userviewall_post(request):
#     lid = request.POST['lid']
#
#     posts = Post.objects.exclude(CUSTOMER__USER_id=lid)
#     edu_contents = EducationalContents.objects.all()
#
#     feed = []
#
#     # Add normal posts
#     for i in posts:
#         feed.append({
#             'id': i.id,
#             'post_type': 'post',
#             'file': i.file,
#             'date': i.date,
#             'description': i.description,
#             'caption': i.caption,
#             'place': i.place,
#             'like': i.like,
#         })
#
#     # Add educational contents
#     for e in edu_contents:
#         feed.append({
#             'id': e.id,
#             'post_type': 'educational',
#             'content': e.content,
#             'date': str(e.date),
#             'time': str(e.time),
#             'type': e.type,
#         })
#
#     # 🔀 Shuffle to make it random
#     random.shuffle(feed)
#
#     return JsonResponse({'status': 'ok', 'data': feed})



import random
from django.http import JsonResponse
from django.db.models import Q

def userviewall_post(request):
    lid = request.POST['lid']
    print(lid)

    accepted_requests = Request.objects.filter(
        Q(Fromr_id=lid, status='accepted') |
        Q(Tor_id=lid, status='accepted')
    ).order_by('-id')

    # Collect user IDs of accepted friends
    accepted_user_ids = set()

    for r in accepted_requests:
        if r.Fromr_id == int(lid):
            accepted_user_ids.add(r.Tor_id)
        else:
            accepted_user_ids.add(r.Fromr_id)

    accepted_customers = Customer.objects.filter(USER_id__in=accepted_user_ids)

    posts = Post.objects.filter(CUSTOMER__in=accepted_customers)

    edu_contents = EducationalContents.objects.all()

    feed = []
    print(posts)
    for i in posts:
        likes=0
        if Likes.objects.filter(POST=i.id).exists():
            likes=Likes.objects.filter(POST=i.id).count()
        feed.append({
            'id': i.id,
            'post_type': 'post',
            'file': i.file,
            'date': i.date,
            'description': i.description,
            'caption': i.caption,
            'place': i.place,
            'like': str(likes),
        })

    # Add educational contents (UNCHANGED ✅)
    for e in edu_contents:
        feed.append({
            'id': e.id,
            'post_type': 'educational',
            'content': e.content,
            'date': str(e.date),
            'time': str(e.time),
            'type': e.type,
        })

    # Shuffle feed
    random.shuffle(feed)

    return JsonResponse({'status': 'ok', 'data': feed})



# def userviewall_post(request):
#     id=request.POST['lid']
#     a=Post.objects.all().exclude(CUSTOMER__USER_id=id)
#     l=[]
#     for i in a:
#         l.append({
#             'id':i.id,
#             'file':i.file,
#             'date':i.date,
#             'description':i.description,
#             'caption':i.caption,
#             'place':i.place,
#             'like':i.like,
#         })
#     return JsonResponse({'status':'ok','data':l})


def likepost(request):
    id = request.POST['id']
    lid = request.POST['lid']
    obj=Likes()
    if Likes.objects.filter(POST_id=id,USER=Customer.objects.get(USER=lid).id).exists():
        Likes.objects.get(POST_id=id, USER=Customer.objects.get(USER=lid).id).delete()
    else:
        obj.POST_id=id
        obj.USER=Customer.objects.get(USER=lid)
        obj.save()

    return JsonResponse({'status': 'ok'})


def addcomment(request):
    lid=request.POST['lid']
    print(lid,"login id")
    comment=request.POST['comment']
    id=request.POST['id']

    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch

    model_name = "Davephoenix/bert-bullying-detector"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    inputs = tokenizer(comment, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    pred = torch.argmax(outputs.logits, dim=1).item()
    pass

    #("Bullying" if pred == 1 else "Not bullying")
    print(pred,"==")
    customer = Customer.objects.get(USER=lid)

    a=Comments()
    if  pred==0:
        b = "normal"
        a.comment = comment
        a.date = datetime.now().today()
        a.POST = Post.objects.get(id=id)
        a.CUSTOMER = customer
        a.status = b
        a.save()
        return JsonResponse({'status': 'ok'})
    else:
        b="toxic"
        return JsonResponse({'status': 'no'})
    




# def viewcomment(request):
#     id=request.POST['id']
#     lid=request.POST['lid']
#     print(id,'scjhsvg')
#     a=Comments.objects.filter(POST_id=id)
#     l=[]
#     for i in a:
#         if Comments.objects.filter(POST__CUSTOMER__USER_id=lid).exists():
#             l.append({
#                 'id':i.id,
#                 'comment':i.comment,
#                 'userid':i.POST.CUSTOMER.id,
#                 'cuid':i.CUSTOMER.USER.id,
#                 'st':'yes'
#             })
#         else:
#             l.append({
#                 'id': i.id,
#                 'comment': i.comment,
#                 'userid': i.POST.CUSTOMER.id,
#                 'st': 'no'
#             })
#     print(l)
#     return JsonResponse({'status':'ok','data':l})


def viewcomment(request):
    id = request.POST['id']     # post id
    lid = request.POST['lid']   # logged in user id

    comments = Comments.objects.filter(POST_id=id)
    data = []

    for i in comments:

        # Comment added user id
        comment_user_id = i.CUSTOMER.USER.id

        # Post owner user id
        post_owner_user_id = i.POST.CUSTOMER.USER.id

        # Check permission
        if int(lid) == comment_user_id or int(lid) == post_owner_user_id:
            status = "yes"   # Can delete
        else:
            status = "no"    # View only

        data.append({
            'id': i.id,
            'comment': i.comment,
            'date': i.date,
            # 'comment_user_id': comment_user_id,
            # 'post_owner_user_id': post_owner_user_id,
            'st': status
        })

    return JsonResponse({'status': 'ok', 'data': data})



# def user_allpost_deletecomment(request):
#     id=request.POST['id']
#     Comments.objects.get(id=id).delete()
#     return JsonResponse({'status':'ok'})

def user_allpost_deletecomment(request):
    cid = request.POST.get('id')
    lid = request.POST.get('lid')

    try:
        comment = Comments.objects.get(id=cid)

        if (comment.CUSTOMER.USER.id == int(lid) or
            comment.POST.CUSTOMER.USER.id == int(lid)):

            comment.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'no permission'})

    except Comments.DoesNotExist:
        return JsonResponse({'status': 'not found'})



def viewOwnpost_comment(request):
    id=request.POST['id']
    print(id,'scjhsvg')
    a=Comments.objects.filter(POST_id=id)
    l=[]
    for i in a:
        l.append({
            'id':i.id,
            'comment':i.comment
        })
    print(l)
    return JsonResponse({'status':'ok','data':l})
#


def sendcomplaint(request):
    complaint=request.POST['complaint']
    id=request.POST['lid']
    obj=Complaints()
    obj.reply='pending'
    obj.complaint=complaint
    obj.status='pending'
    obj.date=datetime.now().today()
    obj.CUSTOMER=Customer.objects.get(USER_id=id)
    obj.save()
    return JsonResponse({'status':'ok'})



def viewreply(request):
    id=request.POST['lid']
    print(id,'scjhsvg')
    a=Complaints.objects.filter(CUSTOMER__USER_id=id)
    l=[]
    for i in a:
        l.append({
            'complaint':i.complaint,
            'date':i.date,
            'status':i.status,
            'reply':i.reply,
        })
    print(l)
    return JsonResponse({'status':'ok','data':l})

def sendappreview(request):
    id = request.POST['lid']
    review = request.POST['review']
    rating = request.POST['rating']
    obj=Review()
    obj.review=review
    obj.rating=rating
    obj.date=datetime.now().today()
    obj.CUSTOMER=Customer.objects.get(USER_id=id)
    obj.save()
    return JsonResponse({'status':'ok'})




def viewreview(request):
    id=request.POST['lid']
    print(id,'scjhsvg')
    a=Review.objects.filter(CUSTOMER__USER_id=id)
    l=[]
    for i in a:
        l.append({
            'review':i.review,
            'date':i.date,
            'rating':i.rating,
        })
    print(l)
    return JsonResponse({'status':'ok','data':l})



def chat_view(request):
    fromid = request.session["lid"]
    toid = request.session["userid"]
    qry = User.objects.get(LOGIN=request.session["userid"])
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid)).order_by('id')
    l = []

    for i in res:
        l.append({"id": i.id, "message": i.message, "to": i.TOID_id, "date": i.date, "from": i.FROMID_id})

    return JsonResponse({'photo': qry.photo, "data": l, 'name': qry.name, 'toid': request.session["userid"]})

def chat_send(request, msg):
    lid = request.session["lid"]
    toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chat()
    chatobt.message = message
    chatobt.TOID_id = toid
    chatobt.FROMID_id = lid
    chatobt.date = d
    chatobt.save()

    return JsonResponse({"status": "ok"})




def User_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    print(FROM_id)
    print(TOID_id)
    msg=request.POST['message']

    from  datetime import datetime
    c=Chat()
    c.FROMID_id=FROM_id
    c.TOID_id=TOID_id
    c.message=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})


def User_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    # lmid = request.POST["lastmsgid"]
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid)).order_by('id')
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.message, "from": i.FROMID_id, "date": i.date, "to": i.TOID_id})

    return JsonResponse({"status":"ok",'data':l})






def android_forget_password(req):
    email = req.POST.get('username')
    if not email:
        return  JsonResponse({'status':'error'})

    try:
        user = User.objects.get(username=email)
        print(email)

        # generate new password
        import random
        new_pass = str(random.randint(1000,9999))
        user.password = make_password(str(new_pass))
        user.save()

        # Email configuration
        smtp_server="smtp.gmail.com"
        smtp_port=587
        sender_email="trainingstarted@gmail.com"
        app_password="nlxasujxgazlbmgz"  # Replace with your actual app password

        # Create email message
        subject ="Your New Password"
        body = f"Your new password is:{new_pass}"
        message= MIMEMultipart()
        message['From']=sender_email
        message['To']=email
        message['Subject']=subject
        message.attach(MIMEText(body, "plain"))

        # send email
        server = smtplib.SMTP(smtp_server,smtp_port)
        server.starttls()
        server.login(sender_email,app_password)
        server.send_message(message)
        server.quit()
        return JsonResponse({'status':'ok'})
    except User.DoesNotExist:
        return JsonResponse({'status':'error'})
    except Exception as e:
        return JsonResponse({'status':'error'})




def reject_notification(request):
    lid= request.POST["nid"]

    k=PostNotification.objects.get(id=lid).POST.id

    if ".mp4" in str(Post.objects.get(id=k).file):
        res = PostNotification.objects.filter(POST_id=k).delete()
        Post.objects.filter(id=k).delete()




    res=PostNotification.objects.filter(id=lid).delete()
    return JsonResponse({'status': 'ok'})

# from pill import Image
def accept_notification(request):
    
    nid= request.POST["nid"]
    n=PostNotification.objects.get(id=nid).POST.file
    pid=PostNotification.objects.get(id=nid).POST.id
    pass#(n)
    bottom=int(PostNotification.objects.get(id=nid).bottom)
    left=int(PostNotification.objects.get(id=nid).left)
    right=int(PostNotification.objects.get(id=nid).right)
    top=int(PostNotification.objects.get(id=nid).top)
    postimage=PostNotification.objects.get(id=nid).POST.file
    postimage=postimage.replace("/media/","")
    imagenews = Image.open("C:\\Kmct\\web\\secureshare\\media\\" + postimage)
    width, height = imagenews.size
    new_image = Image.new("RGB", (width, height))
    def modify_pixel(pixel):
        return (pixel[0] ^ 124, pixel[1] ^ 178, pixel[2] ^ 167)
    for x in range(left, right):
        for y in range(top, bottom):
            pixel = imagenews.getpixel((x, y))
            new_pixel = modify_pixel(pixel)
            imagenews.putpixel((x, y), new_pixel)
    dates= datetime.now().strftime("%Y%m%d%H%M%f")+".bmp"
    p=Post.objects.get(id=pid)
    imagenews.save("C:\\Kmct\\web\\secureshare\\media\\" + dates)
    p.file="/media/"+ dates
    p.save()
    res=PostNotification.objects.filter(id=nid).delete()
    return JsonResponse({'status': 'ok'})




def viewNotification(request):
    nid= request.POST["nid"]
    lid= request.POST["lid"]



    d=PostNotification.objects.filter(USER__USER_id=lid,id__gt=nid).order_by('id')

    if len(d)>0:
        d=d[0]
        return  JsonResponse(
            {
                'status':'ok',
                'nid':str(d.id),
                'message': "A post contain your photo. Please open app and check notificarion page",
            }
        )
    else:
        return JsonResponse(
            {
                'status':'no'

            }
        )
def add_video(request):
    from django.core.files.storage import FileSystemStorage
    from django.http import JsonResponse
    from datetime import datetime
    import cv2
    from PIL import Image
    from ultralytics import YOLO
    import face_recognition
    from transformers import CLIPProcessor, CLIPModel
    import torch
    import  numpy as np

    # ----------- LOAD MODELS -----------
    model_id = "openai/clip-vit-large-patch14"
    model = CLIPModel.from_pretrained(model_id)
    processor = CLIPProcessor.from_pretrained(model_id)
    yolo_model = YOLO("yolov8m.pt")

    # ----------- INPUTS -----------
    file = request.FILES['video']
    description = request.POST['description']
    caption = request.POST['caption']
    place = request.POST['place']
    user_id = request.POST['lid']

    # ----------- SAVE VIDEO -----------
    fs = FileSystemStorage()
    filename = datetime.now().strftime('%Y%m%d-%H%M%S') + ".mp4"
    fs.save(filename, file)

    media_path = "C:\\Kmct\\web\\secureshare\\media\\"
    video_path = media_path + filename
    video_url = fs.url(filename)

    # ----------- EXTRACT ONE FRAME -----------
    cap = cv2.VideoCapture(video_path)

    # Jump to 1 second (better than first frame)
    cap.set(cv2.CAP_PROP_POS_MSEC, 1000)
    notified = set()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # cap.release()

        if not ret:
            return JsonResponse({'status': 'error', 'message': 'Failed to read video'})

        # ----------- SAVE FRAME AS IMAGE -----------
        frame_filename = datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg"
        frame_path = media_path + frame_filename

        cv2.imwrite(frame_path, frame)

        # ----------- CLIP LABELS -----------
        labels = [
            "middle finger gesture",
            "obscene gesture",
            "rude gesture",
            "vulgar pose",
            "offensive sign",
            "abusive behaviour",
            "sexually explicit image",
            "graphic content",
            "safe image"
        ]

        # ----------- CLIP FUNCTION -----------
        def clip_check(frame):
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb)

            inputs = processor(
                text=labels,
                images=image,
                return_tensors="pt",
                padding=True
            )

            with torch.no_grad():
                outputs = model(**inputs)

            probs = torch.softmax(outputs.logits_per_image[0], dim=0)
            print(dict(zip(labels, probs.tolist())))
            return dict(zip(labels, probs.tolist()))

        # ----------- STEP 1: CLIP CHECK -----------
        image = cv2.imread(frame_path)
        # result = clip_check(image)

        # for label, score in result.items():
        #     if label != "safe image" and score > 0.5:
        #         print(label)
        #         return JsonResponse({
        #             'status': 'exp',
        #             'reason': f"{label}: {score:.2f}"
        #         })

        # ----------- LOAD KNOWN USERS -----------
        users = Customer.objects.exclude(USER_id=user_id)

        known_encodings = []
        known_ids = []

        for u in users:
            try:
                img_path = media_path + u.photo.replace("/media/", "")
                img = face_recognition.load_image_file(img_path)
                encoding = face_recognition.face_encodings(img)[0]

                known_encodings.append(encoding)
                known_ids.append(u.id)
            except:
                continue

        # ----------- STEP 2: YOLO + FACE MATCH -----------
        rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = yolo_model(image)



        for result in results:
            for box in result.boxes:

                if int(box.cls[0]) != 0:  # person only
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                person_crop = rgb_frame[y1:y2, x1:x2]
                try:

                    k=0


                    print(type(person_crop), person_crop.shape,"====")


                    #####new code

                    h, w = person_crop.shape[:2]

                    # 🚫 Skip invalid crops
                    if h == 0 or w == 0:
                        continue

                    # 🚫 Skip too small images
                    if h < 50 or w < 50:
                        continue

                    # ✅ Ensure proper format
                    person_crop = np.ascontiguousarray(person_crop)

                    try:
                        face_locations = face_recognition.face_locations(person_crop, model='hog')

                        if len(face_locations) == 0:
                            continue

                        encodings = face_recognition.face_encodings(person_crop, face_locations)


                        ####olde code

                        for encoding in encodings:
                    #
                            matches = face_recognition.compare_faces(
                                known_encodings,
                                encoding,
                                tolerance=0.5
                            )

                        for i, match in enumerate(matches):
                            print(match)
                            if match:
                                uid = known_ids[i]
                                notified.add(uid)



                        #####end old code




                    except Exception as e:
                        print("Face detection error:", e)
                        continue




                    #####end new code






                    # face_locations = face_recognition.face_locations(person_crop)
                    # encodings = face_recognition.face_encodings(person_crop, face_locations)
            #
                #     for encoding in encodings:
                #
                #         matches = face_recognition.compare_faces(
                #             known_encodings,
                #             encoding,
                #             tolerance=0.5
                #         )
                #
                #     for i, match in enumerate(matches):
                #         print(match)
                #         if match:
                #             uid = known_ids[i]
                #             notified.add(uid)
                except Exception as aa:
                    print(aa,"eeeee")

        #             for i, match in enumerate(matches):
        #                 print(match)
        #                 if match:
        #                     uid = known_ids[i]
        #                     notified.add(uid)

    # ----------- SAVE POST -----------

    print("aaaaaa")
    obj = Post()
    obj.file = video_url
    obj.date = datetime.now()
    obj.caption = caption
    obj.description = description
    obj.place = place
    obj.CUSTOMER = Customer.objects.get(USER_id=user_id)
    obj.save()

    print(notified,"===")

    # ----------- SAVE NOTIFICATIONS -----------
    for uid in notified:
        notif = PostNotification()
        notif.POST = obj
        notif.USER_id = uid
        notif.status = "pending"
        notif.date = datetime.now().date()
        notif.save()

    return JsonResponse({'status': 'ok'})

