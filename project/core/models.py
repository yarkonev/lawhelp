import uuid

from django.db import models


class LegalEntity(models.Model):
    firm_id = models.UUIDField(default=uuid.uuid4, editable=False)
    full_name = models.CharField(
        max_length=100, verbose_name='Полное наименование'
    )
    short_name = models.CharField(
        max_length=30, verbose_name='Короткое наименование'
    )
    ogrn = models.CharField(max_length=13, unique=True, verbose_name='ОГРН')
    inn = models.CharField(max_length=10, unique=True, verbose_name='ИНН')
    address = models.TextField(max_length=200, verbose_name='Адрес')

    class Meta:
        abstract = True
        # checks that the OGRN and INN fields matches a specific regex pattern
        # for legal entity identification numbers in Russia.
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    ogrn__regex=r"^[15]\d{2}(?!00)\d{2}\d{7}\d{1}$"
                ),
                name='consistant_ogrn'
            ),
            models.CheckConstraint(
                check=models.Q(
                    inn__regex=r"^(?!00)\d{2}(?!00)\d{2}\d{5}\d{1}$"
                ),
                name='consistant_inn'
            )
        ]


class LegalInstitution(models.Model):
    court_id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='Название суда')
    zip_code = models.CharField(max_length=6, verbose_name='Почтовый индекс')
    address = models.TextField(max_length=200, verbose_name='Адрес')
    account = models.TextField(
        max_length=500, blank=True, verbose_name='Банковские реквизиты'
    )
    relevant_on = models.CharField(
        max_length=50, blank=True, verbose_name='Актуально на'
    )
    reg_id = models.CharField(max_length=2, verbose_name='Код региона')
    reg_name = models.TextField(max_length=100,
                                verbose_name='Название региона')
    compensation = models.DecimalField(max_digits=10,
                                       decimal_places=2,
                                       default=0)

    class Meta:
        abstract = True


class Plaintiff(LegalEntity):
    class Meta:
        verbose_name = 'Истец'
        verbose_name_plural = 'Истцы'

    def __str__(self):
        return self.short_name


class Defendant(LegalEntity):
    class Meta:
        verbose_name = 'Ответчик'
        verbose_name_plural = 'Ответчики'

    def __str__(self):
        return self.short_name


class Court(LegalInstitution):
    class Meta:
        verbose_name = 'Суд первой инстанции'
        verbose_name_plural = 'Суды первой инстанции'

    def __str__(self):
        return self.name


class AppealsCourt(LegalInstitution):
    class Meta:
        verbose_name = 'Апелляционный суд'
        verbose_name_plural = 'Апелляционные суды'

    def __str__(self):
        return self.name


class Case(models.Model):
    case_id = models.UUIDField(default=uuid.uuid4, editable=False)
    number = models.CharField(
        max_length=30, blank=True, null=True, unique=True
    )
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    appeals_court = models.ForeignKey(AppealsCourt, on_delete=models.CASCADE,
                                      blank=True, null=True)
    card = models.URLField(max_length=200, blank=True, null=True, unique=True)
    plaintiff = models.ForeignKey(Plaintiff, on_delete=models.CASCADE)
    defendant = models.ForeignKey(Defendant, on_delete=models.CASCADE)
    overall_charge = models.DecimalField(max_digits=10,
                                         decimal_places=2, default=0)
    gp_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Дело'
        verbose_name_plural = 'Дела'
        constraints = [
            models.UniqueConstraint(
                fields=['court', 'case_id'],
                name='unique_court_case'
            )
        ]

    def __str__(self):
        return f"{self.plaintiff.short_name} - {self.defendant.short_name}"
