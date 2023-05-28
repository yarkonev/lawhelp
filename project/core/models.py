import uuid

from django.db import models


class LegalEntity(models.Model):
    firm_id = models.UUIDField(default=uuid.uuid4, editable=False)
    full_name = models.CharField(
        max_length=100, verbose_name='Полное наименование'
    )
    short_name = models.CharField(
        max_length=30, verbose_name='Сокращенное наименование'
    )
    ogrn = models.CharField(max_length=13, unique=True, verbose_name='ОГРН')
    inn = models.CharField(max_length=10, unique=True, verbose_name='ИНН')
    address = models.TextField(max_length=200, verbose_name='Адрес')

    class Meta:
        abstract = True
        # Checks that the OGRN and INN fields matches a specific regex pattern
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


class Document(models.Model):
    OPTION_CHOICES = [
        ('objection_to_defendant_response', 'Возражение на отзыв ответчика'),
        ('legal_services_contract', 'Договор на оказание юридических услуг'),
        ('application_for_issuance_of_execution_writ', 'Заявление о выдаче исполнительного листа'),
        ('federal_tax_service_request', 'Запрос в ФНС'),
        ('bank_application', 'Заявление в банк'),
        ('application_for_recovery_of_court_costs', 'Заявление о взыскании судебных расходов'),
        ('application_for_duty_setoff', 'Заявление о зачете госпошлины'),
        ('application_for_motivated_decision', 'Заявление о составлении мотивированного решения'),
        ('application_for_enforcement_of_execution_document', 'Заявление об исполнении исполнительного документа'),
        ('envelopes', 'Конверты'),
        ('settlement_agreement', 'Мировое соглашение'),
        ('third_party_explanations', 'Пояснения третьего лица'),
        ('petition', 'Ходатайство'),
        ('motion_for_return_of_complaint', 'Ходатайство о возвращении искового заявления'),
        ('motion_for_retransmission_of_court_order', 'Ходатайство о повторном направлении определения суда'),
        ('motion_for_absentia_review', 'Ходатайство о рассмотрении в отсутствие стороны'),
        ('motion_for_online_participation', 'Ходатайство об участии онлайн'),
        ('appeal_brief', 'Апелляционная жалоба (краткая)'),
        ('case_explanation', 'Объяснение по делу'),
        ('motion_for_submission_of_evidence', 'Ходатайство о приобщении доказательств')
    ]

    option = models.CharField(
        max_length=100, choices=OPTION_CHOICES, verbose_name='Вид документа'
    )

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
    STATUS_CHOICES = (
        ('active', 'В работе'),
        ('completed', 'Завершено'),
        ('no_status', 'Нет статуса'),
    )

    case_id = models.UUIDField(default=uuid.uuid4, editable=False)
    number = models.CharField(
        max_length=30, blank=True, null=True, unique=True
    )
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    appeals_court = models.ForeignKey(
        AppealsCourt, on_delete=models.CASCADE, blank=True, null=True
    )
    card = models.URLField(max_length=200, blank=True, null=True, unique=True)
    plaintiff = models.ForeignKey(Plaintiff, on_delete=models.CASCADE)
    defendant = models.ForeignKey(Defendant, on_delete=models.CASCADE)
    claim_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    gp_charge = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='no_status')

    class Meta:
        verbose_name = 'Дело'
        verbose_name_plural = 'Дела'
        constraints = [
            models.UniqueConstraint(
                fields=['court', 'case_id'], name='unique_court_case'
            )
        ]

    def __str__(self):
        return f"{self.plaintiff.short_name} - {self.defendant.short_name}"
