from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import View,UpdateView,ListView
from scrapboxapp.forms import SignupForm,SigninForm,ProductForm,ProfileForm,BidForm
from django.contrib.auth import authenticate,login,logout
from scrapboxapp.models import ScrapModel,UserProfileModel,WhislistsModel,BidsModel
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import CreateView


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect ("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
# Create your views here.

class RegisterView(CreateView):
    template_name="signup.html"
    form_class=SignupForm
    def post(self,request,*args,**kwargs):
        form=SignupForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request,"Account created successfully")
            return redirect("signin")
        else:
            messages.error(request,"Account creation is failed")
            return render(request,"signup.html",{"form":form})
        
class SigninView(View):
    def get(self,request,*args,**kwargs):
        form=SigninForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=SigninForm(request.POST)
        if form.is_valid():
            uname=request.POST.get("username")
            pwd=request.POST.get("password")
            usr_object=authenticate(request,username=uname,password=pwd)
            if usr_object:
                login(request,usr_object)
                return redirect("home")
        messages.error(request,"Username or password is wrong")
        return render(request,"login.html",{"form":form})
    
@method_decorator(signin_required,name="dispatch")    
class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect ("signin")

@method_decorator(signin_required,name="dispatch")   
class ProductAddView(View):
    def get(self,request,*args,**kwargs):
        form=ProductForm()
        return render(request,"add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=ProductForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            messages.success(request,"Your ad will go live now")
            return redirect("my-ads")
        else:
            messages.success(request,"Ads posting failed")
            return render(request,"add.html",{"form":form})
        
class ProductListView(View):
    def get(self,request,*args,**kwargs):
        qs=ScrapModel.objects.exclude(user=request.user)
        fav_ad=WhislistsModel.objects.get(user=request.user)
        bid=BidsModel.objects.filter(user=request.user)
        count=bid.exclude(status="Pending").count()
        return render (request,"home.html",{"data":qs,"wishlist":fav_ad,"bid_status":bid,"count":count})
    
@method_decorator(signin_required,name="dispatch")
class ProductDetailsView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=ScrapModel.objects.get(id=id)
        fav_ad=WhislistsModel.objects.get(user=request.user)
        bidobj=BidsModel.objects.filter(user=request.user,scrap_id=qs.id)
        bid=BidsModel.objects.filter(user=request.user)
        count=bid.exclude(status="Pending").count()
        return render(request,"scrapdetails.html",{"data":qs,"wishlist":fav_ad,"bid_status":bid,"count":count})
    def post(self,request,*args,**kwargs):  
        id=kwargs.get("pk")
        qs=ScrapModel.objects.get(id=id)
        form=BidForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.instance.scrap=qs
            form.save()
            messages.success(request,"You send a bid")
            return render(request,"scrapdetails.html",{"data":qs,"form":form})
        else:
            messages.success(request,"Bid Sending Failed")
        return render(request,"scrapdetails.html",{"data":qs,"form":form})

@method_decorator(signin_required,name="dispatch")
class MyProductsView(View):
    def get(self,request,*args,**kwargs):
        qs=ScrapModel.objects.filter(user=request.user)
        bid=BidsModel.objects.filter(user=request.user)
        count=bid.exclude(status="Pending").count()
        return render(request,"myprdcts.html",{"data":qs,"bid_status":bid,"count":count})

@method_decorator(signin_required,name="dispatch")
class ProductUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=ScrapModel.objects.get(id=id)
        form=ProductForm(instance=obj)
        return render(request,"pupdate.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=ScrapModel.objects.get(id=id)
        form=ProductForm(request.POST,instance=obj,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Data Updated Successfully")
            return redirect("home")
        else:
            messages.error(request,"Updation failed")
            return render(request,"pupdate.html",{"form":form})
        
@method_decorator(signin_required,name="dispatch")        
class ProductDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        ScrapModel.objects.get(id=id).delete()
        messages.success(request,"Post deleted successfully")
        return redirect("home") 
    
@method_decorator(signin_required,name="dispatch")        
class ProfileUpdateView(UpdateView):
    template_name="profile.html"
    form_class=ProfileForm
    model=UserProfileModel
    def get_success_url(self):
        return reverse("home")

@method_decorator(signin_required,name="dispatch")         
class ProfileDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        user_obj=UserProfileModel.objects.get(id=id)
        qs=ScrapModel.objects.filter(user=id)
        fav_ad=WhislistsModel.objects.get(user=request.user)
        return render(request,"profile_detail.html",{"user":user_obj,"data":qs,"wishlist":fav_ad})
    
@method_decorator(signin_required,name="dispatch")           
class WishlistAddView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        scrap_obj=ScrapModel.objects.get(id=id)
        action=request.POST.get("action")
        wishlist= WhislistsModel.objects.get(user=request.user)
        if action == "add":
            wishlist.scrap.add(scrap_obj)
        elif action == "remove":
            wishlist.scrap.remove(scrap_obj)
        return redirect("home")


@method_decorator(signin_required,name="dispatch") 
class FavAdsView(View):
    def get(self,request,*args,**kwargs):
        qs=WhislistsModel.objects.get(user=request.user)
        ads=ScrapModel.objects.all()
        bid=BidsModel.objects.filter(user=request.user)
        count=bid.exclude(status="Pending").count()
        return render(request,"favourites.html",{"data":qs,"ads":ads,"bid_status":bid,"count":count})
    
@method_decorator(signin_required,name="dispatch")     
class BidListView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=ScrapModel.objects.get(id=id)
        qs=BidsModel.objects.filter(scrap_id=id)
        bid=BidsModel.objects.filter(user=request.user)
        count=bid.exclude(status="Pending").count()
        return render (request,"bid_details.html",{"data":qs,"scrap":data,"bid_status":bid,"count":count})
    
class BidUpdateView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=BidsModel.objects.get(id=id)
        scrap_id=qs.scrap.id
        action=request.POST.get("action")
        if action == "accept":
            BidsModel.objects.filter(id=id).update(status="Accept")
            ScrapModel.objects.filter(id=scrap_id).update(status="Mark as Sold")
        elif action == "reject":
            BidsModel.objects.filter(id=id).update(status="Reject")
            ScrapModel.objects.filter(id=scrap_id).update(status="Available")
        return redirect("home")

    




