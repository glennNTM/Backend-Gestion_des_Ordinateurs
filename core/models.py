from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

# ====================================================
# 🔐 UTILISATEUR PERSONNALISÉ (ADMIN & APPRENANT)
# ====================================================
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('apprenant', 'Apprenant'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='apprenant')
    
    def __str__(self):
        return f"{self.username} ({self.role})"


# ====================================================
# 👤 PROFIL APPRENANT (INFOS SPÉCIFIQUES)
# ====================================================
# Validateur pour le numéro de téléphone (format : exactement 9 chiffres)
phone_validator = RegexValidator(
    regex=r'^\d{9}$',
    message='Le numéro de téléphone doit contenir exactement 9 chiffres.'
)

class ApprenantProfile(models.Model):
    REFERENTIEL_CHOICES = [
        ('DEV_WEB', 'Développeur Web'),
        ('REFERENT_DIGITAL', 'Référent Digital'),
        ('DIGITAL_CREATOR', 'Digital Creator'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='apprenant_profile'
    )
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=100, default='Adresse inconnue')
    referentiel = models.CharField(max_length=100, choices=REFERENTIEL_CHOICES, default='DEV_WEB')
    numero_telephone = models.CharField(max_length=9, unique=True, validators=[phone_validator])

    def __str__(self):
        return f"Profil de {self.user.username}"


# ====================================================
# 💻 ORDINATEUR
# ====================================================
class Ordinateur(models.Model):
    ETAT_CHOICES = [
        ('bon', 'Bon état'),
        ('mineur', 'Problème mineur'),
        ('majeur', 'Problème majeur'),
    ]

    marque = models.CharField(max_length=100, default='Inconnu')
    modele = models.CharField(max_length=100, default='Inconnu')
    processeur = models.CharField(max_length=100, default='Inconnu')
    ram = models.CharField(max_length=100, default='8GB')
    stockage = models.CharField(max_length=100, default='256GB')
    adresse_mac = models.CharField(max_length=100, unique=True, default='00:00:00:00:00:00')
    etat = models.CharField(max_length=10, choices=ETAT_CHOICES, default='bon')

    # Lien avec l'utilisateur apprenant
    apprenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ordinateurs',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.adresse_mac})"


# ====================================================
# 🐞 SIGNALER UN PROBLÈME (ReportIssue)
# ====================================================
class ReportIssue(models.Model):
    TYPE_PROBLEME_CHOICES = [
        ('materiel', 'Problème matériel'),
        ('logiciel', 'Problème logiciel'),
        ('ecran', 'Problème d\'écran'),
        ('clavier', 'Problème de clavier'),
        ('batterie', 'Problème de batterie'),
        ('autre', 'Autre problème'),
    ]

    type_probleme = models.CharField(max_length=20, choices=TYPE_PROBLEME_CHOICES, default='materiel')

    # Lien avec l'utilisateur apprenant
    apprenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports',
        null=True
    )

    # Lien avec l'ordinateur concerné
    ordinateur = models.ForeignKey(
        'Ordinateur',
        on_delete=models.CASCADE,
        related_name='issues'
    )

    description = models.TextField(blank=True, null=True)
    date_signalement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_probleme} signalé par {self.apprenant.username} sur {self.ordinateur.marque}"
