from core.models.user import User
from core.models.user import AdminUser
from core.models.chat import Chatroom
from core.models.message import Message
from core.models.pap_model import PapModel
from core.models.notation import Notation
from core.models.interpretation import Interpretation
from core.models.updating import Updating
from core.models.notification import Notification

from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
# for test
admin.site.register([User])
admin.site.register([AdminUser])
#admin.site.register([Notification,PapModel,Notation,Interpretation,Updating])

#super user
#admin.site.register([User])
# admin_group = Group.objects.create(name='admin_group')
# admin_group.save()
# super_user_1 = User.objects.create_user(username='admin', password='888888', email='xiyue.su@qq.com', is_confirmed=True)
# super_user_1.save()
# admin_group.user_set.add(super_user_1)
#admin_group.permissions.add()
