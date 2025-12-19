from django.db import models

class Promotion(models.Model):
    nom = models.CharField(max_length=50)

    def _str_(self):
        return self.nom


class Etudiant(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name='etudiants'
    )

    def _str_(self):
        return f"{self.prenom} {self.nom}"
