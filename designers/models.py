import django
from django.core import validators
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
import datetime
from phonenumber_field.modelfields import PhoneNumberField


class Designers(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    name = models.CharField("Имя или Название", max_length=500)
    # second_name = models.CharField(max_length=200)
    # middle_name = models.CharField(max_length=200)
    # phone_number = models.CharField("Телефон", max_length=200, validators=[phone_regex], blank=True)
    phone_number = models.CharField("Телефон", max_length=200, blank=True)
    email = models.CharField(max_length=200, validators=[validators.validate_email], blank=True)
    address = models.CharField("Адрес", max_length=500)
    working_area = models.CharField("Место оказания услуг", max_length=500)
    distance_work = models.BooleanField("Удаленная работа?", blank=True, default=False)
    experience = models.DateField("Опыт работы", )
    website = models.CharField("Сайт", max_length=200, null=True, blank=True)
    minimal_order = models.IntegerField("Минимальный заказ", null=True, blank=True)
    description = models.CharField("Описание  деятельности", max_length=1000, null=True, blank=True)
    brigade = models.CharField("Своя бригада/прораб", max_length=1000, null=True, blank=True)
    group = models.BooleanField("Компания?", default=False)
    permissions = (("can_edit_designer",),)

    def get_experience(self):
        return num_years(self.experience)


class PriceList(models.Model):
    designer = models.OneToOneField(
        Designers,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    full_design_project = models.IntegerField("Полный дизайн-проект, за м2", null=True, blank=True)
    supervision = models.IntegerField("Авторский надзор, цена за услугу", null=True, blank=True)
    decorating_of_premises = models.IntegerField("Декорирование помещений, за м2", null=True, blank=True)
    consulting = models.IntegerField("Консультация, цена за улугу", null=True, blank=True)
    working_project = models.IntegerField("Рабочий проект, за м2", null=True, blank=True)
    three_d_visualisation = models.IntegerField("3D визуализация, за м2", null=True, blank=True)

    def get_full_design_project(self):
        try:
            if self.full_design_project < 0:
                return "договорная"
            else:
                return self.full_design_project
        except TypeError:
            return 0

    def get_supervision(self):
        try:
            if self.supervision < 0:
                return "договорная"
            else:
                return self.supervision
        except TypeError:
            return 0

    def get_decorating_of_premises(self):
        try:
            if self.decorating_of_premises < 0:
                return "договорная"
            else:
                return self.decorating_of_premises
        except TypeError:
            return 0

    def get_consulting(self):
        try:
            if self.consulting < 0:
                return "договорная"
            else:
                return self.consulting
        except TypeError:
            return 0

    def get_working_project(self):
        try:
            if self.working_project < 0:
                return "договорная"
            else:
                return self.working_project
        except TypeError:
            return 0

    def get_three_d_visualisation(self):
        try:
            if self.three_d_visualisation < 0:
                return "договорная"
            else:
                return self.three_d_visualisation
        except TypeError:
            return 0


def design_media_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'design_{0}/{1}'.format(instance.designer.id, filename)


def card_media_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'card_of_designer_{0}/{1}'.format(instance.card_of_object.id, filename)


class CardOfObjectForDesigner(models.Model):
    designer = models.ForeignKey(Designers, on_delete=models.CASCADE)
    description = models.CharField("Описание", max_length=500)
    location = models.CharField("Локация", max_length=500)
    budged_from = models.IntegerField("бюджет от", null=True, blank=True)
    budged_to = models.IntegerField("Бюджет до", null=True, blank=True)
    three_d_visualisation = models.FileField("3D визуализация", upload_to=design_media_path)


class Photo(models.Model):
    card_of_object = models.ForeignKey(CardOfObjectForDesigner, on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=255, blank=True)
    description = models.CharField('Описание', max_length=255, blank=True)
    file = models.FileField(upload_to=card_media_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)


def num_years(begin, end=None):
    if end is None:
        end = datetime.datetime.now().date()
    number_of_years = int((end - begin).days / 365.25)
    if begin > years_ago(number_of_years, end):
        return number_of_years - 1
    else:
        return number_of_years


def years_ago(years, from_date=None):
    if from_date is None:
        from_date = datetime.datetime.now().date()
    try:
        return from_date.replace(year=from_date.year - years)
    except ValueError:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29
        return from_date.replace(month=2, day=28,
                                 year=from_date.year - years)
