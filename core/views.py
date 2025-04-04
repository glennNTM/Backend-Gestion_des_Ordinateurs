from rest_framework import viewsets, permissions
from .models import User, Ordinateur, ReportIssue
from .serializers import UserSerializer, OrdinateurSerializer, ReportIssueSerializer

class IsAdmin(permissions.BasePermission):
    """
    Permission personnalisée : autorise seulement les utilisateurs admin.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les utilisateurs.
    Seuls les admins peuvent créer, voir, modifier ou supprimer.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


# ===============================
# 💻 ViewSet pour les Ordinateurs
# ===============================
class OrdinateurViewSet(viewsets.ModelViewSet):
    queryset = Ordinateur.objects.all()
    serializer_class = OrdinateurSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Assigne l'utilisateur connecté comme apprenant lors de la création
        serializer.save(apprenant=self.request.user)


# ===============================
# 🐞 ViewSet pour les ReportIssue
# ===============================
class ReportIssueViewSet(viewsets.ModelViewSet):
    queryset = ReportIssue.objects.all()
    serializer_class = ReportIssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Assigne l'utilisateur connecté comme apprenant lors du signalement
        serializer.save(apprenant=self.request.user)
