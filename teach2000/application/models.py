from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models


# Classificatie van soorten
class Naam(models.Model):
    abstract = True
    naam_nl = models.CharField(max_length=100)
    naam_eng = models.CharField(max_length=100)
    naam_wetenschappelijk = models.CharField(max_length=100)


class Klasse(Naam):
    pass


class Familie(Naam):
    klasse_id = models.ForeignKey(Klasse, on_delete=models.CASCADE)


class Genus(Naam):
    familie_id = models.ForeignKey(Familie, on_delete=models.CASCADE)


class Soort(Naam):
    class MOEILIJKHEIDSGRADEN(models.IntegerChoices):
        ZEER_MAKKELIJK = (1, "Zeer makkelijk")
        MAKKELIJK = (2, "Makkelijk")
        MOEILIJK = (3, "Moeilijk")
        ZEER_MOEILIJK = (4, "Zeer moeilijk")

    genus_id = models.ForeignKey(Genus, on_delete=models.CASCADE)
    moeilijkheidsgraad = models.IntegerField(choices=MOEILIJKHEIDSGRADEN.choices)


class Foto(models.Model):
    soort = models.ForeignKey(Soort, on_delete=models.CASCADE)


class LijktOp(models.Model):
    soort1 = models.ForeignKey(Soort, on_delete=models.CASCADE, related_name="soort1")
    soort2 = models.ForeignKey(Soort, on_delete=models.CASCADE, related_name="soort2")


# Quiz basis modellen


class Quiz(models.Model):
    class QUIZTYPES(models.IntegerChoices):
        STANDAARD = (1, "Standaard")
        VOORBEELD = (2, "Voorbeeld type")

    naam = models.CharField(max_length=100)
    type = models.IntegerField(choices=QUIZTYPES.choices, default=1)


class QuizSessieManager(models.Model):
    def antwoord(self, antwoord: QuizAntwoord):
        sessie, _ = QuizSessie.objects.get_or_create(user=antwoord.user)
        sessie.antwoorden += [antwoord]
        sessie.save()


class QuizVraag(models.Model):
    soort = models.ForeignKey(Soort, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


# quiz sessie basis modellen


class QuizSessie(models.Model):
    objects = QuizSessieManager()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    @property
    def antwoorden(self) -> list[QuizAntwoord]:
        return list(QuizAntwoord.objects.filter(quizsessie=self))

    @property
    def vragen(self) -> list[QuizVraag]:
        return list(QuizVraag.objects.filter(quiz=self.quiz))

    @property
    def score(self) -> int:
        return sum(self.antwoorden)

    @property
    def percentage(self) -> int:
        return int(self.score / len(self.vragen) * 100)

    @property
    def is_completed(self) -> bool:
        return len(self.antwoorden) == len(self.vragen)


class QuizAntwoord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quizvraag = models.ForeignKey(QuizVraag, on_delete=models.CASCADE)
    quizsessie = models.ForeignKey(QuizSessie, on_delete=models.CASCADE)
    antwoord = models.CharField(max_length=100)

    def __init__(
        self,
        antwoord: str,
        *args,
        **kwargs,
    ):
        super().__init__(antwoord=antwoord.lower(), **args, **kwargs)
        SoortScore.antwoord(self)
        QuizSessie.antwoord(self)

    @property
    def correct(self) -> bool:
        vraag = self.vraag
        antwoord = self.antwoord
        return (
            vraag.soort.naam_eng == antwoord
            or vraag.soort.naam_wetenschappelijk == antwoord
            or vraag.soort.naam_nl == antwoord
        )


# Score management modellen

class SoortScoreManager(models.Model):
    def antwoord(self, antwoord: QuizAntwoord):
        score, _ = SoortScore.objects.get_or_create(
            soort=antwoord.quizvraag.soort, user=antwoord.user
        )
        score.antwoorden += [antwoord]
        score.save()


class SoortScore(models.Model):
    objects = SoortScoreManager()

    soort = models.ForeignKey(Soort, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def antwoorden(self) -> list[QuizAntwoord]:
        return list(QuizAntwoord.objects.filter(quizvraag__soort=self))

    @property
    def score(self) -> int:
        return sum(self.antwoorden)
