from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from boards.models import Board
from lists.models import List
from cards.models import Card

class CardTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user1', password='pass1')

        # Obtener token
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url, {'username':'user1','password':'pass1'},format='json')
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Crear board y lista
        self.board = Board.objects.create(name="Test Board", owner=self.user)
        self.board.members.add(self.user)
        self.list = List.objects.create(name="To Do", board=self.board)

    def test_create_card(self):
        url = reverse('list-cards-list', args=[self.board.id, self.list.id])
        data = {"title": "Test Card", "description": "Card desc"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(Card.objects.first().title, "Test Card")

    def test_list_cards(self):
        Card.objects.create(title="Card1", list=self.list)
        Card.objects.create(title="Card2", list=self.list)

        url = reverse('list-cards-list', args=[self.board.id, self.list.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_non_member_cannot_access_cards(self):
        # Crear otro user y otro board
        user2 = User.objects.create_user(username='user2', password='pass2')
        board2 = Board.objects.create(name="Other Board", owner=user2)
        board2.members.add(user2)
        list2 = List.objects.create(name="Another list", board=board2)
        card2 = Card.objects.create(title="Private Card", list=list2)

        url = reverse('list-cards-list', args=[board2.id, list2.id])
        response = self.client.get(url)
        # No debe mostrar nada (no es miembro)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        detail_url = reverse('list-cards-detail', args=[board2.id, list2.id, card2.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 404)
