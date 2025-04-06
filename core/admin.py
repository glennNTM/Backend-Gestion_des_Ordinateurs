from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User, ApprenantProfile, Ordinateur, ReportIssue

# ✅ Personnalisation du modèle User
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ("Rôle utilisateur", {'fields': ('role',)}),
    )

# ✅ (le reste inchangé)
class ApprenantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'referentiel', 'numero_telephone')
    search_fields = ('user__username', 'referentiel', 'numero_telephone')
    list_filter = ('referentiel',)
    raw_id_fields = ('user',)

class OrdinateurAdmin(admin.ModelAdmin):
    list_display = ('marque', 'modele', 'adresse_mac', 'etat', 'apprenant')
    list_filter = ('etat', 'marque')
    search_fields = ('marque', 'modele', 'adresse_mac')
    ordering = ('marque',)

class ReportIssueAdmin(admin.ModelAdmin):
    list_display = ('type_probleme', 'apprenant', 'ordinateur', 'date_signalement')
    list_filter = ('type_probleme', 'date_signalement')
    search_fields = ('apprenant__username', 'ordinateur__adresse_mac')

admin.site.register(User, CustomUserAdmin)
admin.site.register(ApprenantProfile, ApprenantProfileAdmin)
admin.site.register(Ordinateur, OrdinateurAdmin)
admin.site.register(ReportIssue, ReportIssueAdmin)
