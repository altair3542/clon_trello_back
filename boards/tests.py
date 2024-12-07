from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Board

# Create your tests here.

class BoardTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')

        # Obtenemos token
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url, {'username': 'user1', 'password': 'pass1'}, format='json')
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_create_board(self):
        url = reverse('board-list')  # /api/boards/
        data = {"name": "Board Test"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Board.objects.count(), 1)
        board = Board.objects.first()
        self.assertEqual(board.name, "Board Test")
        self.assertIn(self.user, board.members.all())
        self.assertEqual(board.owner, self.user)

    def test_list_boards(self):
        board = Board.objects.create(name="Board Test", owner=self.user)
        board.members.add(self.user)
        url = reverse('board-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Board Test")

    def test_non_member_cannot_see_board(self):
        board = Board.objects.create(name="Board Private", owner=self.user2)
        board.members.add(self.user2)
        # user1 no es miembro
        url = reverse('board-detail', args=[board.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  # No lo ve en su queryset

    def test_update_board(self):
        board = Board.objects.create(name="Old Name", owner=self.user)
        board.members.add(self.user)
        url = reverse('board-detail', args=[board.id])
        data = {"name": "New Name"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        board.refresh_from_db()
        self.assertEqual(board.name, "New Name")
