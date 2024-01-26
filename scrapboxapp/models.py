from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class UserProfileModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    first_name=models.CharField(max_length=100,null=True)
    last_name=models.CharField(max_length=100,null=True)
    contact=models.CharField(max_length=12,null=True)
    pic=models.ImageField(upload_to="pro_pic",null=True,blank=True,default='pro_pic/avatar_2.png')
    def __str__(self):
        return self.user.username
    
class CategoryModel(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class ScrapModel(models.Model):
    name=models.CharField(max_length=100)
    price=models.PositiveIntegerField()
    picture=models.ImageField(upload_to="images")
    category=models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
    location=models.CharField(max_length=100)
    options=(
        ("Like New","Like New"),
        ("Like Good","Like Good"),
        ("Like Fair","Like Fair"),
    )
    condition=models.CharField(max_length=100,choices=options,null=True)
    description=models.CharField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    status_options=(
        ("Mark as Sold","Mark as Sold"),
        ("Available","Available"),
    )
    status=models.CharField(max_length=100,choices=status_options,default="Available")

    def __str__(self):
        return self.name

class WhislistsModel(models.Model):
    scrap=models.ManyToManyField(ScrapModel,related_name="fav_ad")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user

class BidsModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    scrap=models.ForeignKey(ScrapModel,on_delete=models.CASCADE,related_name="bid_scrap")
    amount=models.PositiveIntegerField()
    options=(
        ("Pending","Pending"),
        ("Accept","Accept"),
        ("Reject","Reject"),
    )
    status=models.CharField(max_length=100,choices=options,default="Pending")
    

class ReviewsModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    scrap=models.ForeignKey(ScrapModel,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    rating=models.PositiveIntegerField()

def create_profile(sender,created,instance,**kwargs):
    if created:
        UserProfileModel.objects.create(user=instance)
post_save.connect(create_profile,sender=User)

def create_wishlist(sender,created,instance,**kwargs):
    if created:
        WhislistsModel.objects.create(user=instance)
post_save.connect(create_wishlist,sender=User)