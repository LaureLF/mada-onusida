from django.db import models

TYPES = (('bug', 'Signaler un bug'), ('amélioration', 'Suggérer une amélioration'), ('question', 'Poser une question'), ('commentaire', 'Faire un commentaire'))
GRAVITE = (('1', "1 (C'est un détail)"), ('2','2'), ('3','3'), ('4','4'), ('5','5 (Important)'), ('6','6'), ('7','7'), ('8','8'), ('9','9'), ('10','10 (Essentiel)'))

class Feedback(models.Model):
    type = models.CharField(max_length=50, choices=TYPES, verbose_name="Type d'information à nous transmettre")
    echelle = models.CharField(max_length=10, choices=GRAVITE, verbose_name="Quel est le niveau de gravité de votre problème / question ?")
    description = models.TextField(default=" ", verbose_name="Quel a été le problème rencontré ? Merci de décrire précisément l'action que vous étiez en train d'effectuer")
    suggestion = models.TextField(blank=True, null=True, default=" ", verbose_name="Que souhaitez-vous voir modifier ?")
    nom = nom = models.CharField(max_length=100, verbose_name="Votre nom")
    email = models.EmailField(verbose_name="Votre adresse mail")
    date = models.DateField(auto_now_add=True, null=True)

    class Meta:
        managed = True
        verbose_name = "Bug, suggestion, question ou commentaire"
        verbose_name_plural = "Bugs, suggestions, questions et commentaires"

