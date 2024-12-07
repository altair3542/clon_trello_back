from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import List
from .serializers import ListSerializer
from boards.models import Board

class IsBoardMember(permissions.BasePermission):
    """
    Permite acceso solo a miembros del board asociado a la lista.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.board.members.all()


class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated, IsBoardMember]

    def get_queryset(self):
        # Filtramos las listas por el board id si está en la URL y comprobamos membresía
        board_id = self.kwargs.get('board_pk')  # asumiendo rutas anidadas
        if board_id:
            # Verificar que el usuario es miembro del board
            try:
                board = Board.objects.get(pk=board_id, members=self.request.user)
            except Board.DoesNotExist:
                # Si no es miembro o no existe, devuelve un queryset vacío
                return List.objects.none()

            return board.lists.all()
        else:
            # Si no usamos rutas anidadas, filtrar por usuario
            return List.objects.filter(board__members=self.request.user)

    def perform_create(self, serializer):
        # Obtener el board_id desde la URL (asumiendo rutas anidadas)
        board_id = self.kwargs.get('board_pk')
        board = Board.objects.get(pk=board_id, members=self.request.user)
        serializer.save(board=board)
