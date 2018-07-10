from django.core.mail import send_mail
from example.settings import EMAIL_FROM
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, Contact
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.core.mail import  send_mail
from .forms import EmailPostForm, CommentForm, ContactForm
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, UserEditForm,ProfileEditForm,PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from django.utils.translation import ugettext_lazy as _

def post_detail(request, year, month, day, postit):
    #import pdb;pdb.set_trace()
    all_tags=Tag.objects.all()


    try:
        post = get_object_or_404(Post,slug=postit)
        # publish__year=year,publish__month=month,publish__day=day)
        # the above field lookup are written as in django 1.9 or above
        # publish__year => publish.year
        # publish__month => publish.month
        # publish__day => publish.day
        # And realated model attrebute can also be accessed by
        # author__username => author.username




    except:
        post=Post.published.filter(slug=postit,status='published')#,publish__year=year,publish__month=month,publish__day=day)




    comments=post.comments.filter(active=True)
    '''
        We are using the manager for related objects we defined as comments using the related_name
        attribute of the relationship in the Comment model.
    '''

    #list of similer post
    post_tag_id=post.tags.values_list('id',flat=True)
    similer_post=Post.published.filter(tags__in=post_tag_id).exclude(id=post.id)

    similer_post=similer_post.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:5]
    comment_form=None
    if request.method == 'POST':
        '''
        if the view is called by a GET request we build a form instance with comment_form = CommentForm() .
        If the request is done via POST, we instantiate the form using the
        submitted with comment_form = CommentForm(data=request.POST) data and validate it using
        the is_valid() method
        '''
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            '''
            We create a new Comment object by calling the form's save() method.
            The save() method creates an instance of the model that the form is linked
            to and saves it to the database. If you call it with commit=False , you create
            the model instance, but you don't save it to the database.
            
            The save() method is available for ModelForm but not for
            Form instances, since they are not linked to any model.
            '''
            new_comment = comment_form.save(commit=False)
            '''
            By doing this, we are specifying that the new comment belongs to the
            given post.
            '''
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
        else:
            comment_form = CommentForm()

    return render(request,'blog/post/detail.html',{'post':post,'comments':comments,
                                                   'comment_form':comment_form,
                                                   'similer_post':similer_post,
                                                   'all_tags':all_tags})
                      #{'post': post,'comments': comments,'comment_form': comment_form})

    # return render(request,'blog/post/original_detail.html',{'post': post})
def post_sidebar(request):
    post=Post()
    latest_post=post.published.order_by('-publish')[:5]
    most_commented_post=post.published.annotate(
        total_comment=Count('comments')).order_by('-total_comment')[:5]
    return render(request,'blog/post/latest_post.html',locals())


def post_list(request,tag_slug=None):
    #import pdb;pdb.set_trace()
    all_tags=Tag.objects.all()

    object_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 1 posts in each page
    page = request.GET.get('page')
    try:

        posts = paginator.page(page)


    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'page': page,'posts': posts,'tag':tag,'all_tags':all_tags})




def post_share(request, post_id):
    # Retrieve post by id
    #import pdb;pdb.set_trace();
    from example.settings import EMAIL_FROM
    post = get_object_or_404(Post, id=post_id, status='published')
    sent=False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            post_url=request.build_absolute_uri(post.get_absolute_url())

            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])

            send_mail(subject, message, EMAIL_FROM,[cd['to']])

            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,'form': form,'sent':sent})


def contact(request):
    #import pdb;pdb.set_trace()
    message=''
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            contact_obj = Contact.objects.create(name=cd['name'],email=cd['email'],phone=cd['phone'],query=cd['query'])
            contact_obj.save()
            message='your message send'


    else:
        form=ContactForm()
    return render(request,'site/contact.html',{'form':form,'message':message})

def aboutus(request):
    abtus='we are '
    return render(request,'site/about-us.html',{'about-us':abtus})

def index(request):
    return render(request,'site/index.html')


def signin(request):

    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)

                    return render(request,'site/dashboard.html')
                        #HttpResponse('Authenticated successfully')
                else:
                    message='this account is disabled'
                    #return HttpResponse('Disabled account')
                    return render(request, 'site/login.html', {'form': form, 'message': message})

            else:
                message='either username or password is incorrect'
                #return HttpResponse('Invalid login')
                return render(request, 'site/login.html', {'form': form, 'message':message})
    else:
        form = LoginForm()

    return render(request, 'site/login.html', {'form': form})


@login_required
def dashboard(request):
    #import pdb;pdb.set_trace()
     #we have defined a variable section to track which section of the site the user is watching
    return render(request,'site/dashboard.html',{'section':'dashboard'})

@csrf_exempt
def signup(request):


    #import pdb;pdb.set_trace()

    if request.method=="POST":
        user_form=UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)



            # '''
            # Instead of saving the raw
            # password entered by the user, we use the set_password() method of the User
            # model that handles encryption to save for safety
            # username=cd['username'],
            # '''
            cd=user_form.cleaned_data
            new_user.set_password(cd['password1'])
            new_user.save()

            new_user.user=request.user

            new_user.username=cd['username']
            new_user.first_name=cd['first_name']
            new_user.last_name=cd['last_name']
            new_user.email=cd['email']
            new_user.save()

            profile = Profile.objects.create(user=new_user)
            profile.save()

            #,id=new_user.id)

            #profile.user_id=request.user.id
            #profile.save()
            messages.info(request,'You registered successfully, Now please login')

            return render(request,'site/register_done.html',locals())
        else:
            messages.error(request,'please try agian, data you entered is not valid')
           #return HttpResponse('data you entered is not valid')
    else:
        user_form=UserRegistrationForm()


    return render(request,'site/sign-up.html',locals())

@csrf_exempt
@login_required
def edit(request):
    #import pdb;pdb.set_trace()
    if request.method=='POST':
        user_form=UserEditForm(instance=request.user, data=request.POST)
        profile_form=ProfileEditForm( data=request.POST,
                                     files=request.FILES)#instance=request.user.profile,
        if user_form.is_valid() and profile_form.is_valid():
            save_user=user_form.save()
            save_profile=profile_form.save()
            #profile = Profile.objects.create(user=profile_form)
            messages.success(request,'Profile updated successfully')
            return render(request,'site/dashboard.html',{'message':messages})

        else:
            messages.error(request,'Error updating your profile')

    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm()#instance=request.user.profile)

    return render(request,'site/edit.html',{'user_form':user_form,
                                            'profile_form':profile_form})


def logged_out(request):
    logout(request)
    return render(request,'site/logged_out.html')

def tandc(request):
    return render(request,'site/t-and-c.html')

@login_required
@csrf_exempt
def change_password(request):

    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            # if request.user.is_authenticated():

            user_form=form.save(commit=False)

            cd = user_form.cleaned_data
            user_form.set_password(cd['new_password1'])
            user_form.save()

            user_form.user = request.user
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return render(request,'site/dashboard.html',)
    else:
        form = PasswordChangeForm(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }


    return render(request, 'site/change-password.html', context)

@csrf_exempt
def subscribe(request):
    import pdb;pdb.set_trace()
    if request.method=='POST':
        to_email=request.POST.get("email")
        subject='subject'
        body='body'
        from_email=EMAIL_FROM
        send_mail(subject,body,from_email,[to_email])


    return render(request,'site/index.html')