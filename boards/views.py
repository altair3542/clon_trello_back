from rest_framework import viewsets, permissions
from .models import Board
from .serializers import BoardSerializer, BoardCreateSerializer
from rest_framework.response import Response
from rest_framework import status

class IsBoardMemberOrReadOnly(permissions.BasePermission):
    """
    Permite acceso sólo a miembros del board. Para acciones de lectura, cualquiera con token y miembro puede ver.
    Para acciones de escritura (update, delete), el usuario debe ser miembro. Podríamos en el futuro limitar a owner.
    """
    def has_object_permission(self, request, view, obj):
        # El usuario debe ser miembro del board para cualquier acción.
        return request.user in obj.members.all()

class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsBoardMemberOrReadOnly]

    def get_queryset(self):
        # Mostrar sólo boards en los que el usuario autenticado es miembro
        return Board.objects.filter(members=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return BoardCreateSerializer
        return BoardSerializer

    def perform_create(self, serializer):
        # Al crear un board, el owner es el usuario actual
        board = serializer.save(owner=self.request.user)
        # Agregar el owner como miembro
        board.members.add(self.request.user)

