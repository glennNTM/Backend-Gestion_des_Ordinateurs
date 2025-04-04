from rest_framework import serializers
from .models import User, ApprenantProfile, Ordinateur, ReportIssue

# Serializer du profil apprenant
class ApprenantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprenantProfile
        fields = ['date_naissance', 'adresse', 'referentiel', 'numero_telephone']


# Serializer principal de l'utilisateur
class UserSerializer(serializers.ModelSerializer):
    apprenant_profile = ApprenantProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'apprenant_profile']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # On récupère les données du profil s'il y en a
        profile_data = validated_data.pop('apprenant_profile', None)
        role = validated_data.get('role', 'apprenant')

        # Création de l'utilisateur (hash automatique du mot de passe)
        user = User.objects.create_user(**validated_data)

        # Si l'utilisateur est un apprenant et qu'on a un profil
        if role == 'apprenant' and profile_data:
            ApprenantProfile.objects.create(user=user, **profile_data)

        return user

    def update(self, instance, validated_data):
        # Gestion du mot de passe s'il est mis à jour
        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('apprenant_profile', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        # Mise à jour du profil apprenant si présent
        if profile_data:
            profile = instance.apprenant_profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance



# ================================
# 💻 Serializer pour Ordinateur
# ================================
class OrdinateurSerializer(serializers.ModelSerializer):
    apprenant_username = serializers.CharField(source='apprenant.username', read_only=True)

    class Meta:
        model = Ordinateur
        fields = [
            'id',
            'marque',
            'modele',
            'processeur',
            'ram',
            'stockage',
            'adresse_mac',
            'etat',
            'apprenant',
            'apprenant_username',
        ]
        read_only_fields = ['id', 'apprenant_username']


# ================================
# 🐞 Serializer pour ReportIssue
# ================================
class ReportIssueSerializer(serializers.ModelSerializer):
    ordinateur_mac = serializers.CharField(source='ordinateur.adresse_mac', read_only=True)
    apprenant_username = serializers.CharField(source='apprenant.username', read_only=True)

    class Meta:
        model = ReportIssue
        fields = [
            'id',
            'type_probleme',
            'description',
            'date_signalement',
            'ordinateur',
            'ordinateur_mac',
            'apprenant',
            'apprenant_username',
        ]
        read_only_fields = ['id', 'date_signalement', 'apprenant_username', 'ordinateur_mac']
