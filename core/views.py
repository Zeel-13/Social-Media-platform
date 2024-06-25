from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
# Create your views here.


@login_required(login_url='signin')
def search(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    current_user=[user_profile]

    if request.method == 'POST':
        username=request.POST['username']
        search_text=username
        username_object=User.objects.filter(username__icontains=username)
        username_profile_lists=[]
    
        for username in username_object:
            profile_lists=Profile.objects.filter(user=username)
            username_profile_lists.append(profile_lists)
        
        username_profile_list=list(chain(*username_profile_lists))
        username_profile_list= [ x for x in list(username_profile_list) if x not in current_user ]
        
        return render(request,'search.html',{'user_profile':user_profile,'username_profile_list':username_profile_list,'search_text':search_text})

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower=request.POST['follower']
        user=request.POST['user']
        if FollowersCount.objects.filter(follower=follower,user=user).first():
            delete_follower=FollowersCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower=FollowersCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')


@login_required(login_url='signin')
def profile(request,pk):
    user_object=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_object)
    user_posts=Post.objects.filter(user=pk)
    user_post_length=len(user_posts)

    follower=request.user.username
    user=pk

    if FollowersCount.objects.filter(follower=follower,user=user).first():
        button_text='Unfollow'
    else:
        button_text='Follow'

    user_followers=len(FollowersCount.objects.filter(user=pk))
    user_following=len(FollowersCount.objects.filter(follower=pk))

    context={
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_post_length':user_post_length,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following
    }
    return render(request,'profile.html',context)




@login_required(login_url='signin')
def like_post(request):
    username=request.user.username
    post_id=request.GET.get('post_id')
    post=Post.objects.get(id=post_id)
    like_filter=LikePost.objects.filter(post_id=post_id,username=username).first()
    
    if like_filter == None:
        new_like=LikePost.objects.create(username=username,post_id=post_id)
        new_like.save()
        post.no_of_likes=post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect('/')


@login_required(login_url='signin')
def upload(request):
    if request.method=='POST':
        user=request.user.username
        caption=request.POST['caption']
        image=request.FILES.get('image_upload')
        new_post=Post.objects.create(user=user,caption=caption,image=image)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')



@login_required(login_url="signin")
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    user_following_list=[]
    feed=[]
    
    user_following=FollowersCount.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)
   
    for usernames in user_following_list:
        feed_lists=Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    posts=list(chain(*feed))

    #user suggestions
    all_objects=User.objects.all()
    # print(all_objects)
    user_already_following=[]
    for user in user_following:
        user_list=User.objects.get(username=user.user)
        user_already_following.append(user_list)
    
    new_suggestions=[x for x in list(all_objects) if  (x not in list(user_already_following))]
    current_user=User.objects.filter(username=request.user.username)
    final_suggestions_list= [ x for x in list(new_suggestions) if (x not in list(current_user))]

    random.shuffle(final_suggestions_list)

    # username_profile=[]
    username_profile_list=[]
    # for users in final_suggestions_list:
    #     username_profile.append(users.id)
    # print(username_profile)
    # for ids in username_profile:
    #     profile_lists=Profile.objects.filter(id_user=1)
    #     username_profile_list.append(profile_lists)
    
    for users in final_suggestions_list:
        profile_lists=Profile.objects.filter(user=users)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list=list(chain(*username_profile_list))
    # print(suggestions_username_profile_list)
    return render(request,'index.html',{'user_profile':user_profile,'posts':posts,'suggestions_username_profile_list':suggestions_username_profile_list[:4]})

def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']

        if password==password1:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already taken')
                return redirect('signup')
            else:
                user=User.objects.create(username=username,email=email)
                user.set_password(password)
                user.save()

                # user_login=authenticate(username=username,password=password)
                login(request,user)

                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('setting')
                
        else:
            messages.info(request,'Password not matching')
            return redirect('signup')
    else:
       return render(request,'signup.html')
    
def signin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        # print(username,password)
        # print(user)
        if user is not None:
            # print('success')
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('signin')
    return render(request,'signin.html')

@login_required(login_url="signin")
def logout_user(request):
    logout(request)
    return redirect('signin')

@login_required(login_url="signin")
def setting(request):
    user_profile=Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('profile_image')==None:
            image=user_profile.profile_img
        elif request.FILES.get('profile_image')!=None:
            image=request.FILES.get('profile_image')
        bio=request.POST['bio']
        location=request.POST['location']
        user_profile.profile_img=image
        user_profile.bio=bio
        user_profile.location=location
        user_profile.save()
        return redirect('setting')
    return render(request,'setting.html',{'user_profile':user_profile})

