from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
import json
from django.contrib import messages
from django.core.mail import send_mail
from .forms import UserRegisterForm, CustomUserChangeForm, CustomUserEditForm
from .models import Profile, SubscriptionPlan, UserSubscription
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login as custom_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from movietime.views import user_login_required
from django.conf import settings
from datetime import datetime
import stripe

# Setup Stripe python client library
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


#To do getting the redirect login url from settings.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_admin == False:
            custom_login(request, user)
            return redirect('/')
        else:
            messages.warning(
                request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('login')
    else:
        redirect_to = '/'
        if request.user.is_superuser == False and request.user.is_authenticated:
            return redirect(redirect_to)
        else:
            form = CustomUserChangeForm()
            return render(request, 'login.html', {'title': 'Login', 'form': form})


# Creating a new customer in stripe
def create_customer(payment_method, email):
    customer = stripe.Customer.create (
        payment_method= payment_method,
        email = email,
        invoice_settings={
            'default_payment_method': payment_method,
        }
    )

    return customer

#Creating a new subscription for a customer in stripe
def create_subscription(customer_id, plan_id):
    subscription = stripe.Subscription.create (
        customer = customer_id,
        items = [
            {
                'plan': plan_id,
            }
        ],
        expand=['latest_invoice.payment_intent'],
    )

    return subscription

#Choosing the type of plan you want to signup with
def choose_plan(request):
    if request.user.is_superuser == False and request.user.is_authenticated:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    premium_plan = SubscriptionPlan.objects.filter(membership_type='Premium').first()
    free_plan = SubscriptionPlan.objects.filter(membership_type='Free').first()

    context = {
        'title': 'Choose Plan',
        'free_plan': free_plan,
        'premium_plan': premium_plan,
    }

    return render(request, 'editplan.html', context)

#Reviewing the subscription before registering
def review_subscription(request, subscription_type):
    if request.user.is_superuser == False and request.user.is_authenticated:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    premium_plan = SubscriptionPlan.objects.filter(membership_type=subscription_type).first()

    context = {
        'title': 'Review Plan',
        'plan': premium_plan,
    }

    return render(request, 'checkout.html', context)


#Register either with premium or free account
def register(request, plan):
    if request.user.is_superuser == False and request.user.is_authenticated:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        context = {
            'title': 'Sign Up',
            'form': form,
            'plan': plan,
        }
        if form.is_valid():
            if plan == 'Premium':
                try: 
                    payment_method = request.POST.get('paymentMethod')
                    email = form.cleaned_data['email']
                    # Creating a new customer for payment
                    customer = create_customer(payment_method, email)

                    # Creating a subscription plan for the customer
                    plan = SubscriptionPlan.objects.get(membership_type='Premium')
                    subscription = create_subscription(customer.id, plan.stripe_plan_id)

                    user = form.save()
                    profile = Profile.objects.get(id=user.id)

                    # Saving the user subscription information in database
                    user_subscription = UserSubscription()
                    user_subscription.user = profile
                    user_subscription.stripe_customer_id = customer.id
                    user_subscription.subscription_plan = plan
                    user_subscription.stripe_subscription_id = subscription.id
                    user_subscription.save()

                    #Sending email upon successful registration
                    subject = 'Congratulations!! Your account has been successfully created.'
                    message = 'You are subscribed to the premium access. You will be charged $15 monthly.'
                    from_mail = 'MovieTime'
                    email_to = profile.email
                    send_mail(subject, message, from_mail, [email_to])
                    
                    username = form.cleaned_data.get('username')
                    messages.success(request, f'Account created for {username}!')
                    return redirect('login')
                except stripe.error.APIConnectionError as e:
                    messages.warning(request, 'Sorry couldn\'t register right now. Internal server error. Try agan later.')
                    return redirect('login')
                except stripe.error.RateLimitError as e:
                    messages.warning(request, 'Sorry couldn\'t register right now. Internal server error. Try agan later.')
                    return redirect('login')
                except stripe.error.AuthenticationError as e:
                    messages.warning(request, 'Sorry couldn\'t register right now. Internal server error. Try agan later.')
                    return redirect('login')
                except stripe.error.StripeError as e:
                    messages.warning(request, 'Sorry couldn\'t register right now. Internal server error. Try agan later.')
                    return redirect('login')
            elif plan == 'Free':
                form.save()
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')

                #Sending email upon successful registration
                subject = 'Congratulations!! Your account has been successfully created.'
                message = 'You are subscribed to the free access. You can upgrade your account in the future if you wish.'
                from_mail = 'MovieTime'
                email_to = email
                send_mail(subject, message, from_mail, [email_to])

                messages.success(request, f'Account created for {username}!')
                return redirect('login')
    else:
        form = UserRegisterForm()
        context = {
            'title': 'Sign Up',
            'form': form,
            'plan': plan,
        }
    return render(request, 'register.html', context)


@user_login_required
def profile(request):
    context = {}
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    context['title'] = full_name

    user = Profile.objects.get(id=request.user.id)
    subscription_status = UserSubscription.objects.filter(user=user).exists()

    context['plan_exists'] = subscription_status

    if subscription_status == True:
        try:
            user_sub = UserSubscription.objects.get(user=user)
            sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)


            context['status'] = sub.status
            context['billing'] = sub.billing

            cancelled_at_unix = sub.ended_at
            start_date_unix = sub.current_period_start
            end_date_unix = sub.current_period_end
            ts1 = int(start_date_unix)
            ts2 = int(end_date_unix)
            if cancelled_at_unix is not None:
                ts3 = int(cancelled_at_unix)
                context['cancelled_at'] = datetime.utcfromtimestamp(ts3).strftime('%Y-%m-%d %H:%M:%S')

            context['start_date'] = datetime.utcfromtimestamp(ts1).strftime('%Y-%m-%d %H:%M:%S')
            context['end_date'] = datetime.utcfromtimestamp(ts2).strftime('%Y-%m-%d %H:%M:%S')
            

            # Plan information
            context['plan'] = sub['items'].data[0].plan.active
            context['currency'] = sub['items'].data[0].plan.currency
            context['trial'] = sub['items'].data[0].plan.trial_period_days
            context['product_id'] = sub['items'].data[0].plan.product
            
        except stripe.error.APIConnectionError as e:
            context['stripe_error'] = e
            messages.warning(request, 'Couldn\'t retrieve account plan information. Internal server error.')
            return render(request, 'profile/user_profile.html', context)
        except stripe.error.RateLimitError as e:
            context['stripe_error'] = e
            messages.warning(request, 'Couldn\'t retrieve account plan information. Internal server error.')
            return render(request, 'profile/user_profile.html', context)
        except stripe.error.AuthenticationError as e:
            context['stripe_error'] = e
            messages.warning(request, 'Couldn\'t retrieve account plan information. Internal server error.')
            return render(request, 'profile/user_profile.html', context)
        except stripe.error.StripeError as e:
            context['stripe_error'] = e
            messages.warning(request, 'Couldn\'t retrieve account plan information. Internal server error.')
            return render(request, 'profile/user_profile.html', context)
        
    return render(request, 'profile/user_profile.html', context)


@user_login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserEditForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Profile has been updated.')
            return redirect('profile')
        else:
            messages.warning(
                request, f'Make sure you enter the form details properly')
            return redirect('edit_profile')
    else:
        form = CustomUserEditForm(instance=request.user)
        return render(request, 'profile/edit_profile.html', {'title': 'Edit Profile', 'form': form})


@user_login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, f'Password has been changed.')
            return redirect('profile')
        else:
            messages.warning(
                request, f'Make sure remember your old password and enter the new password properly')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'profile/change_password.html', {'title': 'Change Password','form': form})


@user_login_required
def settings(request):
    return render(request, 'profile/settings.html', {'title': 'Profile Settings'})


@user_login_required
def del_user(request):
    try:
        user = Profile.objects.get(username=request.user.username)
        user_sub = UserSubscription.objects.get(user=user)

        if user_sub is not None:
            try: 
                cust = stripe.Customer.retrieve(user_sub.stripe_customer_id)
                cust.delete()
            except stripe.error.APIConnectionError as e:
                messages.info(request, 'Sorry, could not delete user. Try again later')
                return redirect('profile')
            except stripe.error.RateLimitError as e:
                messages.info(request, 'Sorry, could not delete user. Try again later')
                return redirect('profile')
            except stripe.error.AuthenticationError as e:
                messages.info(request, 'Sorry, could not delete user. Try again later')
                return redirect('profile')
            except stripe.error.StripeError as e:
                messages.info(request, 'Sorry, could not delete user. Try again later')
                return redirect('profile')

        user.delete()

        messages.success(request, f'User is deleted.')
        return redirect('login')

    except Exception as e:
        messages.warning(request, e.message)
        return redirect('profile')

#Upgrade the account for free to premium
@user_login_required
def upgrade_account(request):
    user = Profile.objects.get(id=request.user.id)
    subscribed = UserSubscription.objects.filter(user=user).exists()

    if not subscribed:
        premium_plan = SubscriptionPlan.objects.filter(membership_type='Premium').first()

        context = {
            'plan': premium_plan,
            'title': 'Upgrade: Premium Plan',
        }
        return render(request, 'upgradeplan.html', context)
    else:
        messages.info(request, f'You plan has already been upgraded')
        return redirect('profile')

@user_login_required
def upgrade(request):
    user = Profile.objects.get(id=request.user.id)
    subscribed = UserSubscription.objects.filter(user=user).exists()

    if not subscribed:
        if request.method == 'POST':
            try:
                payment_method = request.POST.get('paymentMethod')
                user = Profile.objects.get(id=request.user.id)

                # Creating a new customer for payment
                customer = create_customer(payment_method, user.email)

                # Creating a subscription plan for the customer
                plan = SubscriptionPlan.objects.get(membership_type='Premium')
                subscription = create_subscription(customer.id, plan.stripe_plan_id)

                profile = Profile.objects.get(id=user.id)

                # Saving the user subscription information in database
                user_subscription = UserSubscription()
                user_subscription.user = profile
                user_subscription.stripe_customer_id = customer.id
                user_subscription.subscription_plan = plan
                user_subscription.stripe_subscription_id = subscription.id
                user_subscription.save()

                messages.info(request, f'Your plan has been upgraded to premium. Enjoy!!')
                return redirect('profile')
            except stripe.error.APIConnectionError as e:
                messages.warning(request, 'Sorry upgrade failed. Couldn\'t communicate with the payment gateway.')
                return redirect('profile')
            except stripe.error.RateLimitError as e:
                messages.warning(request, 'Sorry upgrade failed. Internal Server error.')
                return redirect('profile')
            except stripe.error.AuthenticationError as e:
                messages.warning(request, 'Sorry upgrade failed. Internal Server error.')
                return redirect('profile')
            except stripe.error.StripeError as e:
                messages.warning(request, 'Sorry upgrade failed. Internal Server error.')
                return redirect('profile')
    else:
        messages.info(request, f'You already have an subscription!!')
        return redirect('profile')


#Cancel the subscription of the user
@user_login_required
def cancel_subscription(request):
    user = Profile.objects.get(id=request.user.id)
    user_sub = UserSubscription.objects.get(user=user)

    if user_sub is not None:
        if user_sub.active == False:
            messages.info(request, f'You don\'t have an active subscription')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        try:
            sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
            sub.delete()

            user_sub.active = False
            user_sub.save()

            free_plan = SubscriptionPlan.objects.filter(membership_type="Free").first()
            user_subscription = UserSubscription.objects.get(user=user)
            user_subscription.subscription_plan = free_plan
            user_subscription.save()

            messages.info(request, "Successfully cancelled subscription")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except stripe.error.APIConnectionError as e:
            messages.warning(request, 'Sorry cancellation failed. Internal Server error.')
            return redirect('profile')
        except stripe.error.RateLimitError as e:
            messages.inwarningfo(request, 'Sorry cancellation failed. Internal Server error.')
            return redirect('profile')
        except stripe.error.AuthenticationError as e:
            messages.warning(request, 'Sorry cancellation failed. Internal Server error.')
            return redirect('profile')
        except stripe.error.StripeError as e:
            messages.warning(request, 'Sorry cancellation failed. Internal Server error.')
            return redirect('profile')
    else:
        messages.info(request, f'You don\'t have a premium plan')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


#Reactivate the subscription of the user
@user_login_required
def reactivate_subscription(request):
    user = Profile.objects.get(id=request.user.id)
    user_sub = UserSubscription.objects.get(user=user)

    if user_sub is not None:
        if user_sub.active == True:
            messages.info(request, f'You have an active subscription plan')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        try:
            premium_plan = SubscriptionPlan.objects.filter(membership_type="Premium").first()
            # Creating a new subscription for the customer
            subscription = create_subscription(user_sub.stripe_customer_id, premium_plan.stripe_plan_id) 

            start_date_unix = subscription.start_date
            ts = int(start_date_unix)
            start_date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print(start_date)

            user_sub.active = True
            user_sub.subscription_plan = premium_plan
            user_sub.stripe_subscription_id = subscription.id
            user_sub.save()

            messages.info(request, "You subscription has been activated since %s" %(start_date))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except stripe.error.APIConnectionError as e:
            messages.warning(request, 'Sorry activation failed. Internal Server error.')
            return redirect('profile')
        except stripe.error.RateLimitError as e:
            messages.warning(request, 'Sorry activation failed. Internal Server error.')
            return redirect('profile')
        except stripe.error.AuthenticationError as e:
            messages.warning(request, 'Sorry activation failed. Internal Server error.')
            return redirect('profile')
        except stripe.error.StripeError as e:
            messages.warning(request, 'Sorry activation failed. Internal Server error.')
            return redirect('profile')

    else:
        messages.info(request, f'You don\'t have a premium plan')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
