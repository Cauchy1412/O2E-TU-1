"""
define the url routes of core api
"""
from django.urls import path
from core.api.auth import obtain_jwt_token, refresh_jwt_token
from core.api.chat import get_chat_list, delete_chat, message_read, create_chat, get_chat, push_message
from core.api.friend import list_friends, list_full_friends

from core.api.my_post import list_posts
from core.api.profile import get_profile
from core.api.search import search_user_list,search_user_full_list
from core.api.sign_up import change_password, change_email, CREATE_USER_API, FORGET_PASSWORD_API
from core.api.comment import create_comment, delete_comment, get_comment, get_comment_list
from core.api.demand import create_demand,  get_demand_list, get_demand

from core.api.user import follow, unfollow, list_favorite_recent, change_organization

from core.api.fan import list_fans, list_full_fans
from core.api.follower import list_followers, list_full_followers
from core.api.user_icon import USER_ICON_API,read_img,read_default_img
from core.api.notification import (NOTIFICATION_API, NOTIFICATION_SET_API)
from core.api.image import (IMAGE_API, IMAGE_SET_API)

from core.api.interpretation import createInterpretation, INTERPRETATION_API, \
  collectInterpretation, uncollectInterpretation, likeInterpretation, searchInterpretation, \
    transmitInterpretation, recommendInterpretation, downloadInterpretation, randomWalkInterpretation, \
      getAllInterpretation, queryVisitorNumber, queryKeywordTops, queryTagRatio

from core.api.user import get_all_user_info,delete_user,change_user_info,get_user_info

urlpatterns = [

    #user apis
    path('token-auth', obtain_jwt_token),
    path('token-refresh', refresh_jwt_token),
    path('user/create', CREATE_USER_API),
    path('user/change-password', change_password),
    path('user/change-email', change_email),
    path('user/forget-password', FORGET_PASSWORD_API),
    path('user/profile', get_profile),
    path('user/icon', USER_ICON_API),
    path('user/all',get_all_user_info),
    path('user/delete',delete_user),
    path('user/changeinfo',change_user_info),
    path('user/get-user-info',get_user_info),
    
    # demand apis
    path('demand/create', create_demand),
    path('demand', get_demand_list),
    path('demand/<int:id>', get_demand),

    # comment apis
    path('comment/create', create_comment),
    path('comment/delete', delete_comment),
    path('comment/<int:id>', get_comment),
    path('comment', get_comment_list),

      # user apis
    path('user/<int:pid>/follow', follow),
    path('user/<int:pid>/unfollow', unfollow),
    path('user/organization', change_organization),
    # collection apis
    path('favorites/page/<int:pindex>', list_favorite_recent),


    # list posts - web PAGE
    path('post/<int:uid>', list_posts),

    #list fans - web PAGE
    path('fan/<int:uid>', list_fans),
    #list fans - app ROLL
    path('fan/roll/<int:uid>', list_full_fans),

    #list follower - web PAGE
    path('follower/<int:uid>', list_followers),
    #list follower - app ROLL
    path('follower/roll/<int:uid>', list_full_followers),


    #list friends - web PAGE
    path('friend/<int:uid>', list_friends),
    #list friends - app ROLL
    path('friend/roll/<int:uid>', list_full_friends),

    # notifications
    path('notification', NOTIFICATION_API),
    path('notification/page/<int:pindex>', NOTIFICATION_SET_API),

    # recommend related
    path('recommend', recommendInterpretation),
    path('Interpretation/popup', randomWalkInterpretation),

    # images
    path('image', IMAGE_API),
    path('image/page/<int:pindex>', IMAGE_SET_API),

    #chat
    path('chat/create',create_chat),
    path('chat/<int:id>', get_chat),
    path('chat/list', get_chat_list),
    path('chat/delete', delete_chat),
    path('chat/read', message_read),
    path('chat/push',push_message),

    #search - web PAGE
    path('user/search/<int:uid>',search_user_list),
    # search - app ROLL
    path('user/search/roll',search_user_full_list),

    # interpretations
    path('Interpretation', createInterpretation),
    path('Interpretation/<int:id>', INTERPRETATION_API),
    path('Interpretation/<int:eid>/favor', collectInterpretation),
    path('Interpretation/<int:eid>/unfavor', uncollectInterpretation),
    path('Interpretation/<int:id>/like', likeInterpretation),
    path('Interpretation/page/<int:pid>', searchInterpretation),
    path('Interpretation/<int:id>/transmit', transmitInterpretation),
    path('Interpretation/getall', getAllInterpretation),
    path('Interpretation/getvis', queryVisitorNumber),
    path('Interpretation/getkeywords', queryKeywordTops),
    path('Interpretation/gettags', queryTagRatio),

    #image
    path('images/<str:year>/<str:day>/icons/<str:file_name>',read_img),
    path('images/default_user_icon.jpg',read_default_img),

    # downloads
    path('download/Interpretation/<int:id>', downloadInterpretation),

]

