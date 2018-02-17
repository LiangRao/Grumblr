from django.db import models
from django.utils import timezone
from datetime import datetime
from django.db.models import Max
from django.utils.html import escape

# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name="profile")
	age = models.IntegerField(default=18, blank=True)
	about = models.TextField(max_length=20000, default='', blank=True)
	picture = models.ImageField(upload_to='profile-pictures', default='', blank=True)
	follows = models.ManyToManyField(User, related_name='followees', symmetrical=False)
	def __unicode__(self):
		return self.user


class Post(models.Model):
	user = models.ForeignKey(User, related_name='posts')
	text = models.TextField(max_length=20000)
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.text

	@staticmethod
	def get_posts_user(user, time="1970-01-01T00:00+00:00"):
		return Post.objects.filter(user=user, deleted=False, 
			   date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_posts_global_stream(user, time="1970-01-01T00:00+00:00"):
		return Post.objects.exclude(user=user).filter(deleted=False, 
			   date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_posts_follower_stream(user, time="1970-01-01T00:00+00:00"):
		user_profile = UserProfile.objects.get(user=user)
		following = user_profile.follows.all()
		return Post.objects.filter(user__in=following, deleted=False, 
			   date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_max_time_user(user):
		return Post.objects.filter(user=user).aggregate(Max('date_created'))['date_created__max'] or "1970-01-01T00:00+00:00"

	@staticmethod
	def get_max_time_global_stream(user):
		return Post.objects.exclude(user=user).aggregate(Max('date_created'))['date_created__max'] or "1970-01-01T00:00+00:00"

	@staticmethod
	def get_max_time_follower_stream(user):
		user_profile = UserProfile.objects.get(user=user)
		following = user_profile.follows.all()
		return Post.objects.filter(user__in=following).aggregate(Max('date_created'))['date_created__max'] or "1970-01-01T00:00+00:00"

	@staticmethod
	def get_changes_user(user, time="1970-01-01T00:00+00:00"):
		return Post.objects.filter(user=user, date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_changes_global_stream(user, time="1970-01-01T00:00+00:00"):
		return Post.objects.exclude(user=user).filter(date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_changes_follower_stream(user, time="1970-01-01T00:00+00:00"):
		user_profile = UserProfile.objects.get(user=user)
		following = user_profile.follows.all()
		return Post.objects.filter(user__in=following, 
			   date_created__gt=time).distincct().order_by('-date_created').reverse()

	@property
	def html(self):
		return "<li class='post_item' id='post_%d'> <div class='form'> <img src='/profile-picture/%s' width='50px'> %s %s <br>%s<h4>%s</h4><textarea class='form-control' type='text' placeholder='Write something...' name='comment' id='new-comment'></textarea>\
          <button id='comment-btn'>Comment</button><ul style='list-style-type: none' id='comment-list'></ul></div></li>" % (self.id, escape(self.user.id), escape(self.user.first_name), escape(self.user.last_name), self.date_created, escape(self.text))
	
	# Generates the HTML-representation of a single to-do list item.
	# @property
	# def html(self):
	# 	return "<li id='post_%d'> <button class='delete-btn'>x</button> %s</li>" % (self.id, self.text)

class Comment(models.Model):
	user = models.ForeignKey(User, related_name='comments') #the commenter
	post = models.ForeignKey(Post, related_name='comments') #the post being commented on
	deleted = models.BooleanField(default=False)
	text = models.TextField(max_length=20000)
	date_created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.text

	@staticmethod
	def get_comments(post, time="1970-01-01T00:00+00:00"):
		return Comment.objects.filter(post=post, deleted=False, 
			           date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_changes(post, time="1970-01-01T00:00+00:00"):
		return Comment.objects.filter(post=post, date_created__gt=time).distinct().order_by('-date_created').reverse()

	# @property
	# def html(self):
	# 	return "<hr><li id='comment_%d'><img src='profile_picture/%d' width='50px'>%s %s<br>%s<p>%s</p></li>" % (self.id, escape(self.user.id), escape(self.user.first_name), escape(self.user.last_name), self.date_created, escape(self.text))

	@property
	def html(self):
		return "<hr><li id='comment_%d'><img src='/profile-picture/%s' width='50px'> %s %s <br>%s<h4>%s</h4>\
          </li>" % (self.id, escape(self.user.id), escape(self.user.first_name), escape(self.user.last_name), self.date_created, escape(self.text))
	

	@staticmethod
	def get_max_time(post):
		return Comment.objects.filter(post=post).aggregate(Max('date_created'))['date_created__max'] or "1970-01-01T00:00+00:00"