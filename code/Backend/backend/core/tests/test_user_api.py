from rest_framework.test import (APITestCase,
                                 APIRequestFactory,
                                 force_authenticate
                                 )
from core.models.user import User


class TestUserModel(APITestCase):
    fixtures = ['initial.json', 'users.json']

    def setUp(self) -> None:
        print('test user apis')
        self.user1 = User.objects.get(pk=10001)
        self.user2 = User.objects.get(pk=10002)
        self.factory = APIRequestFactory()

    def tset_follow_api(self):
        # self.assertEqual(len(self.user2.get_fan()), 0)
        # request = self.factory.post("user/" + str(self.user2.id) + "/follow", {})
        # force_authenticate(request, self.user1)
        # view = FollowView.as_view()
        # response = view(request)
        # print(response)
        pass
