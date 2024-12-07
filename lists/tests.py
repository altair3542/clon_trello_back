from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from boards.models import Board
from lists.models import List

class ListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user1', password='pass1')
        # Obtener token
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url, {'username':'user1','password':'pass1'},format='json')
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Crear un board
        self.board = Board.objects.create(name="Test Board", owner=self.user)
        self.board.members.add(self.user)

    def test_create_list(self):
        url = reverse('board-lists-list', args=[self.board.id]) # /api/boards/<board_id>/lists/
        data = {"name": "To Do"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(List.objects.count(), 1)
        self.assertEqual(List.objects.first().name, "To Do")

    def test_list_lists(self):
        list_obj = List.objects.create(name="To Do", board=self.board)
        url = reverse('board-lists-list', args=[self.board.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "To Do")

    def test_non_member_cannot_access_lists(self):
        # Crear otro usuario y otro board
        user2 = User.objects.create_user(username='user2', password='pass2')
        board2 = Board.objects.create(name="Other Board", owner=user2)
        board2.members.add(user2)
        List.objects.create(name="Another To Do", board=board2)

        # Intentar listar las listas de board2 con user1 (no miembro)
        url = reverse('board-lists-list', args=[board2.id])
        response = self.client.get(url)
        # Debe devolver 200 pero lista vacía o 404?
        # Con la lógica actual, no habrá queryset. Retorna vacío.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        # Intentar GET detalle de la lista
        list_obj = board2.lists.first()
        detail_url = reverse('board-lists-detail', args=[board2.id, list_obj.id])
        response = self.client.get(detail_url)
        # Como no encuentra la lista en el queryset filtrado, debe dar 404
        self.assertEqual(response.status_code, 404)
