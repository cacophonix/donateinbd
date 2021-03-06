


from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from forms import RegistrationForm
from forms import AuthenticateForm
from forms import PostDonationForm
from django.contrib.auth.decorators import login_required
from models import UserProfile
from models import Post
from models import ProfileFeedback
from models import Message
from models import PostFeedback
from django.views.generic import ListView
from django.views.generic import View
from inspect import getmembers
from pprint import pprint









# Create your views here.



class IndexView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'post_list'


    def get_queryset(self, *args, **kwargs):
        return Post.objects.all()

    def get_context_data(self,**kwargs):

        context = super(IndexView, self).get_context_data(**kwargs)

        context['auth_form']  = kwargs.get('auth_form',None) or AuthenticateForm()

        # messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        # if len(messages) <=5:
        #     message5 = messages
        # else :
        #     message5 = messages[:5]
        #
        # message5=message5[::-1]

        context['auth_form']  = kwargs.get('auth_form',None) or AuthenticateForm()
        # context['message5']  = message5

        return context







def index(request, auth_form = None):

    # if not request.user.is_authenticated():

    auth_form = auth_form or AuthenticateForm()

    # return IndexView.as_view()

    post_list =  Post.objects.all()

    messages5 = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))[::5]
    if len(messages5) <=5:
        message5 = messages5
    else :
        message5 = messages5[:5]
    # message5=message5[::-1]

    # print(auth_form.error_messages())


    return render(request, 'home.html',{'post_list':post_list, 'user':request.user, 'auth_form':auth_form, 'message5':message5})


@login_required()
def my_donation_view(request):

    post_list = Post.objects.all().filter(user=request.user)
    messages5 = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))[::-1]
    if len(messages5) <=5:
        message5 = messages5
    else :
        message5 = messages5[:5]

    # message5=message5[::-1]

    return render(request, 'home.html',{'post_list':post_list, 'user':request.user,'message5':message5})


def donation_view(request, auth_form = None):

    post_list = Post.objects.all().filter(post_type="make donation")
    messages5 = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))[::-1]
    if len(messages5) <=5:
        message5 = messages5
    else :
        message5 = messages5[:5]

    # message5=message5[::-1]

    return render(request, 'donations.html',{'post_list':post_list, 'user':request.user, 'auth_form':auth_form, 'message5':message5})


def request_donation_view(request, auth_form = None):

    post_list = Post.objects.all().filter(post_type="take donation")
    messages5 = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))[::-5]
    if len(messages5) <=5:
        message5 = messages5
    else :
        message5 = messages5[:5]

    # message5=message5[::-1]

    return render(request, 'requests.html',{'post_list':post_list, 'user':request.user, 'auth_form':auth_form, 'message5':message5})





def register(request,register_form=None):

    if request.method == "GET":

        # print(register_form)

        form = AuthenticateForm(data=request.POST)

        register_form = register_form or RegistrationForm()

        print(register_form)

        return render(request, 'register.html', {'register_form':register_form})

    if request.method == 'POST':

        register_form=RegistrationForm(data=request.POST)

        if register_form.is_valid():

            username = register_form.clean_username()
            password = register_form.clean_password2()

            register_form.save()

            user = authenticate(username=username, password=password)

            userprofile = UserProfile(user=user)

            userprofile.save()

            login(request,user)

            return redirect('/dashboard')

        else:

            return register(request,register_form=register_form)


def login_view(request):

    if request.method=="POST":
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            return index(request, auth_form=form)
        else :
            return index(request, auth_form=form)

    return redirect('/dashboard')


@login_required()
def logout_view(request):
    logout(request)
    return redirect('/')




@login_required()
def post_donation_view(request, post_donation_form=None):
    post_donation_form = post_donation_form or PostDonationForm()
    messages5 = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))[::-1]
    if len(messages5) <=5:
        message5 = messages5
    else :
        message5 = messages5[:5]

    # message5=message5[::-1]

    return render(request,'post_donation.html',{'post_donation_form': post_donation_form , 'message5':message5})




@login_required()
def submit_donation_view(request):

    userprofile = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PostDonationForm(data=request.POST)

        if form.is_valid():
            post=form.save(commit=False)
            post.user=UserProfile(user=request.user)
            post.user_id= User.objects.get(username=request.user).pk
            print post.user_id
            post.save()
            # form.save_m2m()
            redirect('/dashboard')
        else :
            post_donation_view(request, form)
    # print request

    return redirect('/dashboard')


def post_detail_view(request,pk=1,auth_form=None):
    auth_form = auth_form or AuthenticateForm()
    post = Post.objects.get(pk=pk)
    messages5 = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))[::-1]
    if len(messages5) <=5:
        message5 = messages5
    else :
        message5 = messages5[:5]

    cur_profile = (str(request.user) == str(post.user.user.username))

    # print request.user
    # print post.user.user.username
    # print cur_profile

    # user=User.objects.get(username = request.user)
    # userprofile = UserProfile.objects.get(user=user)


    report_list = Report.objects.filter(working_project = post )

    # print cur_profile,report_list


    # message5=message5[::-1]
    if post.post_type == 'make donation':
		return render(request,'donation_detail.html',{'post':post, 'user':request.user, 'auth_form': auth_form, 'message5':message5,'cur_profile':cur_profile,'report_list':report_list})
    else:
		return render(request,'donation_req_detail.html',{'post':post, 'user':request.user, 'auth_form': auth_form, 'message5':message5,'cur_profile':cur_profile,'report_list':report_list})


@login_required()
def profile_detail_view(request,username=None,auth_form=None):

    auth_form = auth_form or AuthenticateForm()
    user = User.objects.get(username=username)
    UserProfile.objects.get_or_create(user=user)
    profile = UserProfile.objects.get(user=user)
    profile_feedback = ProfileFeedback.objects.all().filter(user=user)

    messages5 = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))[::-1]
    if len(messages5) <=5:
        message5 = messages5
    else :
        message5 = messages5[:5]

    # message5=message5[::-1]


    return render(request, 'profile.html', {'profile':profile, 'user':request.user, 'auth_form': auth_form, 'profile_feedback': profile_feedback, 'message5':message5})


@login_required()
def my_profile(request):

    auth_form = AuthenticateForm()
    user = User.objects.get(username=request.user)
    UserProfile.objects.get_or_create(user=user)
    profile = UserProfile.objects.get(user=user)
    profile_feedback = ProfileFeedback.objects.all().filter(user=user)
    messages5 = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))[::-1]
    if len(messages5) <=5:
        message5 = messages5
    else :
        message5 = messages5[:5]

    # message5=message5[::-1]

    return render(request, 'my_profile.html', {'profile':profile, 'user':request.user, 'auth_form': auth_form, 'profile_feedback': profile_feedback, 'message5':message5})



def all_users_view(request,auth_form = None):

    auth_form = auth_form or AuthenticateForm()

    user_list = User.objects.all()

    messages5 = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))[::-1]

    if len(messages5) <=5:
        message5 = messages5
    else :
        message5 = messages5[:5]

    # message5=message5[::-1]

    return render(request, 'users.html', {'message5':message5, 'user_list':user_list, 'auth_form': auth_form})





def add_profile_feedback(request):

    # print('hic')
    #
    feedback=ProfileFeedback()
    #
    feedback.message=request.POST['message']
    feedback.feedback_sender=request.user or "Annonymous"
    feedback.user = User.objects.get(username=request.POST['profile'])

    feedback.save()



    # pprint(getmembers(feedback))
    return HttpResponse("success")

@login_required()
def my_messages(request):

    # print('hic')
    #
    messages = Message.objects.filter(Q(sender=User.objects.get(username=request.user)) | Q(receiver=request.user))
    auth_form = AuthenticateForm()

    profile=User.objects.all().get(username=request.user)

    messages5 = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))[::-1]
    if len(messages5) <=5:
        message5 = messages5
    else :
        message5 = messages5[:5]

    # message5=message5[::-1]




    return render(request, 'all_message.html', {'messages':messages,'message5':message5, 'profile':profile, 'auth_form':auth_form })


from forms import UserProfileUpdateForm

@login_required()
def update(request, update_form= None):

    # print('hic')
    #

    if request.method == "GET":

        user = User.objects.get(username=request.user)

        userprofile = UserProfile.objects.get(user=user)

        auth_form = AuthenticateForm()
        update_form = update_form or UserProfileUpdateForm(instance=userprofile)




        update_form.fields['first_name'].initial = user.first_name
        update_form.fields['last_name'].initial = user.last_name
        update_form.fields['email'].initial = user.email


        messages5 = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))[::-1]

        if len(messages5) <=5:
            message5 = messages5
        else :
            message5 = messages5[:5]

        # message5=message5[::-1]

        return render(request, 'update.html', {'update_form':update_form, 'auth_form':auth_form, 'message5':message5 })

    if request.method == "POST":

        update_form=UserProfileUpdateForm(request.POST,request.FILES)

        user = User.objects.get(username=request.user)

        if user.check_password(update_form.data['password']) and update_form.is_valid():

            user.first_name=update_form.cleaned_data['first_name']
            user.last_name=update_form.cleaned_data['last_name']
            user.email=update_form.cleaned_data['email']
            user.website=update_form.cleaned_data['website']
            user.donor_donee_type=update_form.cleaned_data['donor_donee_type']
            user.image=update_form.cleaned_data['image']
            user.occupation=update_form.cleaned_data['occupation']
            user.description=update_form.cleaned_data['description']
            user.country=update_form.cleaned_data['country']
            user.city=update_form.cleaned_data['city']
            user.street_address=update_form.cleaned_data['street_address']
            user.contact_no=update_form.cleaned_data['contact_no']
            user.street_no=update_form.cleaned_data['street_no']

            user.save()

            #~ print "hic"
            return my_profile(request)
        else :
            request.method="GET"

            update_form.fields['password'].widget.attrs.update({'class': 'error'})

            print update_form

            return update(request,update_form)





from django.db.models import Q

class send_message(View):



    def get(self, request, **kwargs):


        # print (request.user)
        # print (kwargs['receiver'])

        messages = Message.objects.filter(Q(sender=request.user, receiver=kwargs['receiver']) | Q(sender=User.objects.get(username=kwargs['receiver']), receiver=request.user))



        profile = User.objects.filter(username=kwargs['receiver'])[0]



        auth_form = AuthenticateForm()

        messages5 = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))[::-1]
        if len(messages5) <=5:
            message5 = messages5
        else :
            message5 = messages5[:5]

        # message5=message5[::-1]



        # print profile

        return render(request, 'message.html', {'messages':messages, 'profile':profile, 'auth_form':auth_form, 'message5':message5 })



    def post(self, request, **kwargs):

        file = request.FILES.get('file')
        content = request.POST.get('message')
        sender = request.user
        message = Message()

        message.file=file


        # print message.file

        message.content=content
        message.receiver = kwargs['receiver']
        message.sender=User.objects.get(username=sender)
        message.sender_full_name = message.sender.userprofile.get_full_name()
        print message.sender_full_name
        message.save()

        # print message
        #
        # print message.file


        # print (request.user)

        messages = Message.objects.filter(Q(sender=request.user, receiver=kwargs['receiver']) | Q(sender=User.objects.get(username=kwargs['receiver']), receiver=request.user))

        messages5 = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))[::-1]
        if len(messages5) <=5:
            message5 = messages5
        else :
            message5 = messages5[:5]

        # message5=message5[::-1]

        # print profile

        profile = User.objects.filter(username=kwargs['receiver'])[0]

        auth_form = AuthenticateForm()


        return render(request, 'message.html', {'messages':messages, 'profile':profile ,'auth_form':auth_form, 'message5':message5})


from forms import ReportForm
from models import Report

@login_required()
def show_report(request,report_id=None):

    report = Report.objects.get(pk=report_id)

    return render(request, 'show_report.html', {'report': report})



@login_required()
def submit_report(request):

    if request.method == "GET":

        submit_report_form = ReportForm()
        # print submit_report_form
        return render(request,'submit_report.html', {'submit_report_form':submit_report_form})

    if request.method == 'POST':

        submit_report_form = ReportForm(request.POST,request.FILES)

        print submit_report_form

        if submit_report_form.is_valid():

            report = submit_report_form.save(commit=False)
            report.profile=UserProfile.objects.get(user=request.user)
            report.save()


            return show_report(request, report_id=report.id)


        return render(request,'submit_report.html', {'submit_report_form':submit_report_form})



@login_required()
def show_report_list(request,post_id=None):
	
    report_list = Report.objects.filter(post=post_id)

    return render(request,'show_report_list.html',{'report_list':report_list})





def first_page(request):
	
	post_list = Post.objects.all().filter(post_type="take donation")
	req_len = len(post_list)
	if len(post_list) > 2:
		post_list = post_list[:2]
	
	don_post_list = Post.objects.all().filter(post_type="make donation")
	don_len = len(don_post_list)
	if len(don_post_list) > 2:
		don_post_list = don_post_list[:2]
		
	auth_form = AuthenticateForm()
	
	
	return render(request,'first_page.html', {'req_post_list':post_list,'offer_post_list':don_post_list,'req_len':req_len,'don_len':don_len,'auth_form':auth_form})








































