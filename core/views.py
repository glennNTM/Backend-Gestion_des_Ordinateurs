from rest_framework import viewsets, permissions
from .models import User, Ordinateur, ReportIssue
from .serializers import UserSerializer, OrdinateurSerializer, ReportIssueSerializer

# ✅ Permission pour les admins uniquement
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

# ✅ Autoriser les utilisateurs à accéder uniquement à leurs propres données
class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or obj == request.user

# ✅ Pour vérifier si l'ordinateur appartient à l'utilisateur
class IsOwnerOrdinateurOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or obj.apprenant == request.user

# ✅ Pour vérifier si le report appartient à l'utilisateur
class IsOwnerReportOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or obj.apprenant == request.user

# ===============================
# 👤 User ViewSet
# ===============================
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'create', 'destroy']:
            return [IsAdmin()]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return [permissions.IsAuthenticated(), IsSelfOrAdmin()]
        return [permissions.IsAuthenticated()]

# ===============================
# 💻 Ordinateur ViewSet
# ===============================
class OrdinateurViewSet(viewsets.ModelViewSet):
    serializer_class = OrdinateurSerializer

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Ordinateur.objects.all()
        return Ordinateur.objects.filter(apprenant=self.request.user)

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerOrdinateurOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(apprenant=self.request.user)

# ===============================
# 🐞 ReportIssue ViewSet
# ===============================
class ReportIssueViewSet(viewsets.ModelViewSet):
    serializer_class = ReportIssueSerializer

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return ReportIssue.objects.all()
        return ReportIssue.objects.filter(apprenant=self.request.user)

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerReportOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(apprenant=self.request.user)
