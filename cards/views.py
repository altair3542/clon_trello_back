from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Card
from .serializers import CardSerializer
from lists.models import List
from boards.models import Board

# Create your views here.
class IsBoardMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj es una Card
        # Verificamos membresía en el board asociado a la lista de la card
        return request.user in obj.list.board.members.all()

class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated, IsBoardMember]

    def get_queryset(self):
        # Necesitamos filtrar las tarjetas por el list_id, que viene de la URL
        # Asumimos rutas anidadas: /api/boards/<board_id>/lists/<list_id>/cards/
        board_id = self.kwargs.get('board_pk')
        list_id = self.kwargs.get('list_pk')

        # Primero verificar que el usuario sea miembro del board
        try:
            board = Board.objects.get(pk=board_id, members=self.request.user)
        except Board.DoesNotExist:
            return Card.objects.none()

        # Verificar que la lista pertenezca a ese board
        try:
            lst = board.lists.get(pk=list_id)
        except List.DoesNotExist:
            return Card.objects.none()

        return lst.cards.all()

    def perform_create(self, serializer):
        board_id = self.kwargs.get('board_pk')
        list_id = self.kwargs.get('list_pk')

        board = Board.objects.get(pk=board_id, members=self.request.user)
        lst = board.lists.get(pk=list_id)
        serializer.save(list=lst)
