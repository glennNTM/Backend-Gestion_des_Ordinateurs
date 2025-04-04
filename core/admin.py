from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User, ApprenantProfile, Ordinateur, ReportIssue

# ✅ Personnalisation du modèle User
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

# ✅ Personnalisation du modèle ApprenantProfile
class ApprenantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'referentiel', 'numero_telephone')
    search_fields = ('user__username', 'referentiel', 'numero_telephone')
    list_filter = ('referentiel',)
    
    # Permet d'éditer directement les champs liés
    raw_id_fields = ('user',)

# ✅ Personnalisation du modèle Ordinateur
class OrdinateurAdmin(admin.ModelAdmin):
    list_display = ('marque', 'modele', 'adresse_mac', 'etat', 'apprenant')
    list_filter = ('etat', 'marque')
    search_fields = ('marque', 'modele', 'adresse_mac')
    ordering = ('marque',)

# ✅ Personnalisation du modèle ReportIssue
class ReportIssueAdmin(admin.ModelAdmin):
    list_display = ('type_probleme', 'apprenant', 'ordinateur', 'date_signalement')
    list_filter = ('type_probleme', 'date_signalement')
    search_fields = ('apprenant__username', 'ordinateur__adresse_mac')

# ✅ Enregistrement des modèles avec leurs classes personnalisées
admin.site.register(User, CustomUserAdmin)
admin.site.register(ApprenantProfile, ApprenantProfileAdmin)
admin.site.register(Ordinateur, OrdinateurAdmin)
admin.site.register(ReportIssue, ReportIssueAdmin)
