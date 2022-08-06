from __future__ import annotations

from random import sample

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
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

    @property
    def klasse(self):
        return self.klasse_id


class Genus(Naam):
    familie_id = models.ForeignKey(Familie, on_delete=models.CASCADE)

    @property
    def familie(self):
        return self.familie_id

    @property
    def klasse(self):
        return self.familie.klasse


class Soort(Naam):
    class MOEILIJKHEIDSGRADEN(models.IntegerChoices):
        ZEER_MAKKELIJK = (1, "Zeer makkelijk")
        MAKKELIJK = (2, "Makkelijk")
        MOEILIJK = (3, "Moeilijk")
        ZEER_MOEILIJK = (4, "Zeer moeilijk")

    genus_id = models.ForeignKey(Genus, on_delete=models.CASCADE)
    moeilijkheidsgraad = models.IntegerField(choices=MOEILIJKHEIDSGRADEN.choices)

    @property
    def genus(self):
        return self.genus_id

    @property
    def familie(self):
        return self.genus.familie

    @property
    def soort(self):
        return self.genus.klasse

    @property
    def lijkt_op(self) -> list[Soort]:
        return list(LijktOp.objects.filter(soort1=self)) + list(
            LijktOp.objects.filter(soort2=self)
        )

    @property
    def lijkt_een_beetje_op(self) -> list[Soort]:
        lijkt_op = self.lijkt_op
        lijkt_een_beetje_op = []
        for soort in lijkt_op:
            lijkt_een_beetje_op += soort.lijkt_op
        return list(set(lijkt_een_beetje_op))

    def meerkeuze_opties(self, aantal: int) -> list[Soort]:
        lijkt_op = self.lijkt_op
        if len(lijkt_op) >= aantal:
            return sample(self.lijkt_op, aantal)
        potentiele_soorten = lijkt_op + self.lijkt_een_beetje_op
        if len(potentiele_soorten) >= aantal:
            return sample(potentiele_soorten, aantal)
        soort_ids = [soort.id for soort in potentiele_soorten]
        potentiele_soorten += list(
            sample(
                Soort.objects.exclude(pk__in=soort_ids),
                len(potentiele_soorten) - aantal,
            )
        )
        return potentiele_soorten


class Foto(models.Model):
    soort = models.ForeignKey(Soort, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to="fotos", blank=True)


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

    def meerkeuze_vraag(self, soort: Soort, aantal: int = 5):
        meerkeuze_opties = soort.meerkeuze_opties(aantal=aantal)
        QuizVraag(soort=soort, quiz=self, opties=meerkeuze_opties)


class QuizVraag(models.Model):
    soort = models.ForeignKey(Soort, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    meerkeuze_opties = ArrayField(Soort, max_length=20, null=True)


# quiz sessie basis modellen


class QuizSessieManager(models.Model):
    def antwoord(self, antwoord: QuizAntwoord):
        sessie, _ = QuizSessie.objects.get_or_create(user=antwoord.user)
        sessie.antwoorden += [antwoord]
        sessie.save()


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
        SoortScore.objects.antwoord(self)
        QuizSessie.objects.antwoord(self)

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


class SoortScoreManager(models.Manager):
    def antwoord(self, antwoord: QuizAntwoord):
        score, _ = SoortScore.objects.get_or_create(
            soort=antwoord.quizvraag.soort, user=antwoord.user
        )
        score.antwoorden.append(antwoord)
        score.save()


class SoortScore(models.Model):
    objects = SoortScoreManager()

    soort = models.ForeignKey(Soort, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def antwoorden(self) -> list[QuizAntwoord]:
        return list(QuizAntwoord.objects.filter(quizvraag__soort=self.soort))

    @property
    def score(self) -> int:
        return sum(self.antwoorden)
