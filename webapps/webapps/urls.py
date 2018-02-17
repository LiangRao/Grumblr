"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
import grumblr.views

urlpatterns = [
	url(r'^$', grumblr.views.global_stream, name='stream'),
    url(r'^follower-stream$', grumblr.views.follower_stream, name='follower-stream'),
    url(r'^profile/(?P<user_id>\d+)$', grumblr.views.profile, name='profile'),

    # Route for built-in authentication with our own custom login page
    url(r'^login$', views.login, {'template_name':'grumblr/login.html'}, name='login'),


    # Reset password
    url(r'^reset$', views.password_reset, {'template_name':'grumblr/password_reset_form.html',
                                           'from_email':'hsuehlin+huang@andrew.cmu.edu',
                                           'post_reset_redirect':'/reset/done'},
                                           name='password_reset'),
    url(r'^reset/done$', views.password_reset_done, {'template_name':'grumblr/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.password_reset_confirm, 
        {'template_name':'grumblr/password_reset_confirm.html', 'post_reset_redirect':'/done'}, 
        name='password_reset_confirm'),
    url(r'^done$', views.password_reset_complete, {'template_name':'grumblr/password_reset_complete.html'}, name='reset_complete'),



    url(r'^profile-picture/(?P<user_id>\d+)$', grumblr.views.profile_picture, name='profile-picture'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', views.logout_then_login, name='logout'),
    url(r'^register$', grumblr.views.register, name='register'),
    url(r'^add-post$', grumblr.views.add_post, name='add-post'),
    url(r'^delete-post/(?P<post_id>\d+)$', grumblr.views.delete_post, name='delete-post'),
    url(r'^edit-profile$', grumblr.views.edit_profile, name='edit-profile'),

    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', grumblr.views.confirm_registration, name='confirm-registration'),
    url(r'^follow/(?P<following_id>\d+)$', grumblr.views.follow, name='follow'),
    url(r'^unfollow/(?P<unfollowing_id>\d+)$', grumblr.views.unfollow, name='unfollow'),
    #url(r'^comment/(?P<redirect_name>\w+)/(?P<user_id>\d+)/(?P<post_id>\d+)$', grumblr.views.comment, name='comment'),

    url(r'^get-profile-posts/(?P<user_id>\d+)$', grumblr.views.get_profile_posts, name='get-profile-posts'),
    url(r'^get-global-stream-posts$', grumblr.views.get_global_stream_posts, name='get-global-stream-posts'),
    url(r'^get-follower-stream-posts$', grumblr.views.get_follower_stream_posts, name='get-follower-stream-posts'),
    url(r'^get-profile-posts/(?P<user_id>\d+)/(?P<time>.+)$', grumblr.views.get_profile_posts, name='get-profile-posts'),
    url(r'^get-global-stream-posts/(?P<time>.+)$', grumblr.views.get_global_stream_posts, name='get-global-stream-posts'),
    url(r'^get-follower-stream-posts/(?P<time>.+)$', grumblr.views.get_follower_stream_posts, name='get-follower-stream-posts'),
    
    # url(r'^get-posts/(?P<username>[A-Za-z]\w*)/(?P<post_id>\d+)$', grumblr.views.get_posts, name='get-posts-username-post-id'),
    # url(r'^get-posts/(?P<username>[A-Za-z]\w*)$', grumblr.views.get_posts, name='get-posts-username'),

    url(r'^get-profile-changes/(?P<user_id>\d+)/$', grumblr.views.get_profile_changes, name='get-profile-changes'),
    url(r'^get-global-stream-changes$', grumblr.views.get_global_stream_changes, name='get-global-stream-changes'),
    url(r'^get-follower-stream-changes$', grumblr.views.get_follower_stream_changes, name='get-follower-stream-changes'),
    url(r'^get-profile-changes/(?P<user_id>\d+)/(?P<time>.+)$', grumblr.views.get_profile_changes, name='get-profile-changes'),
    url(r'^get-global-stream-changes/(?P<time>.+)$', grumblr.views.get_global_stream_changes, name='get-global-stream-changes'),
    url(r'^get-follower-stream-changes/(?P<time>.+)$', grumblr.views.get_follower_stream_changes, name='get-follower-stream-changes'),
    
    # url(r'^get-changes/(?P<post_id>\d+)$', grumblr.views.get_changes, name='get-changes-post-id'),

    # url(r'^get-comments$', grumblr.views.get_comments),
    url(r'^get-comments/(?P<post_id>\d+)$', grumblr.views.get_comments),
    url(r'^get-comments/(?P<post_id>\d+)/(?P<time>.+)$', grumblr.views.get_comments),
    url(r'^get-comment-changes/(?P<post_id>\d+)/$', grumblr.views.get_comment_changes),
    url(r'^get-comment-changes/(?P<post_id>\d+)/(?P<time>.+)$', grumblr.views.get_comment_changes),
    url(r'^add-comment/(?P<post_id>\d+)$', grumblr.views.add_comment),
]
