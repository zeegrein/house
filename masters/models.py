import django
from django.core import validators
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
import datetime

STATUS_CHOICES = (
    ("Кыргызстан", ("Кыргызстан")),
    ("Казахстан", ("Казахстан")),
)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    slug = models.CharField(max_length=10, unique=True,
                            default="question")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Master(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Придерживайтесь формата'+996 312 111 222'. до 16 цифр.")
    first_name = models.CharField('Имя', max_length=200)
    second_name = models.CharField('Фамилия', max_length=200, null=True, blank=True, default=None)
    middle_name = models.CharField('Отчество', max_length=200, null=True, blank=True, default=None)
    phone_number = models.CharField('Телефон', max_length=200, help_text='ввести международный формат')
    email = models.CharField(max_length=200, validators=[validators.validate_email], null=True, blank=True,
                             help_text='электронная почта')
    city = models.CharField('Город', max_length=200)
    country = models.CharField('Страна', max_length=200, choices=STATUS_CHOICES, default=1)
    experience = models.DateField('Опыт работы', null=True, blank=True, default=None,
                                  help_text='с какого года или сколько полных лет')
    additional_info = models.CharField('Дополнительная информация', max_length=1000, null=True, blank=True,
                                       default=None)
    group = models.BooleanField("Бригадир?", default=False,
                                help_text="Есть ли своя бригада. Отметить если есть, иначе пропустить")

    def get_experience(self):
        return num_years(self.experience)

        # def save(self, *args, **kwargs):
        #     for var in vars(self):
        #         if not var.startswith('_'):
        #             if self.__dict__[var] == '':
        #                 self.__dict__[var] = None
        #     super(Master, self).save(*args, **kwargs)


class PriceForRemodeling(models.Model):
    master = models.OneToOneField(Master, on_delete=models.CASCADE, primary_key=True)
    overhaul = models.IntegerField('Капитальный ремонт без перепланировки ', blank=True, null=True)
    remodeling = models.IntegerField('Косметический ремонт ', null=True, blank=True, )
    party_remodeling = models.IntegerField('Частичный ремонт ', null=True, blank=True, )

    def get_overhaul(self):
        try:
            if self.overhaul < 0:
                return "Договорная"
            else:
                return self.overhaul
        except TypeError:
            return 0

    def get_remodeling(self):
        try:
            if self.remodeling < 0:
                return "Договорная"
            else:
                return self.remodeling
        except TypeError:
            return 0

    def get_party_remodeling(self):
        try:
            if self.party_remodeling < 0:
                return "Договорная"
            else:
                return self.party_remodeling
        except TypeError:
            return 0


class PriceForWallsAndCeiling(models.Model):
    master = models.OneToOneField(Master, on_delete=models.CASCADE)
    alignment = models.IntegerField('Выравнивание', blank=True, null=True)
    plaster = models.IntegerField('Штукатурка', blank=True, null=True)  # штукатурка
    putty = models.IntegerField('Шпатлевка и шлифовка под окраску', blank=True, null=True)  # шпатлевка
    undercoat = models.IntegerField('Грунтовка', blank=True, null=True)  # грунтовка
    colorizing_ceil_and_walls = models.IntegerField('Покраска', blank=True, null=True)
    ceiling_skirting_boards = models.IntegerField('Установка потолочного плинтуса', blank=True, null=True)
    wallpaper = models.IntegerField('Поклейка обоев', blank=True, null=True)

    def get_alignment(self):
        try:
            if self.alignment < 0:
                return "Договорная"
            else:
                return self.alignment
        except TypeError:
            return 0

    def get_plaster(self):
        try:
            if self.plaster < 0:
                return "Договорная"
            else:
                return self.plaster
        except TypeError:
            return 0

    def get_putty(self):
        try:
            if self.putty < 0:
                return "Договорная"
            else:
                return self.putty
        except TypeError:
            return 0

    def get_undercoat(self):
        try:
            if self.undercoat < 0:
                return "Договорная"
            else:
                return self.undercoat
        except TypeError:
            return 0

    def get_colorizing_ceil_and_walls(self):
        try:
            if self.colorizing_ceil_and_walls < 0:
                return "Договорная"
            else:
                return self.colorizing_ceil_and_walls
        except TypeError:
            return 0

    def get_ceiling_skirting_boards(self):
        try:
            if self.ceiling_skirting_boards < 0:
                return "Договорная"
            else:
                return self.ceiling_skirting_boards
        except TypeError:
            return 0

    def get_wallpaper(self):
        try:
            if self.wallpaper < 0:
                return "Договорная"
            else:
                return self.wallpaper
        except TypeError:
            return 0


class PriceForTiling(models.Model):
    master = models.OneToOneField(Master, on_delete=models.CASCADE, unique=True)
    surface_preparation = models.IntegerField('Подготовка поверхности', blank=True, null=True)
    tailing = models.IntegerField('Укладка плитки', blank=True, null=True)
    bathroom_fully = models.IntegerField('Санузел под ключ', blank=True, null=True)
    stacking_of_porcelain_tiles = models.IntegerField('	Укладка керамогранита', blank=True, null=True)
    stacking_of_maze = models.IntegerField('Укладка мозайки', blank=True, null=True)
    grout = models.IntegerField('Затирка швов', blank=True, null=True)

    def get_surface_preparation(self):
        try:
            if self.surface_preparation < 0:
                return "Договорная"
            else:
                return self.surface_preparation
        except TypeError:
            return 0

    def get_tailing(self):
        try:
            if self.tailing < 0:
                return "Договорная"
            else:
                return self.tailing
        except TypeError:
            return 0

    def get_bathroom_fully(self):
        try:
            if self.bathroom_fully < 0:
                return "Договорная"
            else:
                return self.bathroom_fully
        except TypeError:
            return 0

    def get_stacking_of_porcelain_tiles(self):
        try:
            if self.stacking_of_porcelain_tiles < 0:
                return "Договорная"
            else:
                return self.stacking_of_porcelain_tiles
        except TypeError:
            return 0

    def get_stacking_of_maze(self):
        try:
            if self.stacking_of_maze < 0:
                return "Договорная"
            else:
                return self.stacking_of_maze
        except TypeError:
            return 0

    def get_grout(self):
        try:
            if self.grout < 0:
                return "Договорная"
            else:
                return self.grout
        except TypeError:
            return 0


def master_media_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'master_{0}/{1}'.format(instance.master.id, filename)


class CardOfObjectForMaster(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    description = models.CharField('Описание', max_length=500)
    location = models.CharField('Локация', max_length=500)
    budged_from = models.IntegerField('Бюджет от', null=True, blank=True, default=0)
    budged_to = models.IntegerField('Бюджет до', null=True, blank=True, default=0)
    image = models.FileField(upload_to=master_media_path)

    def __str__(self):
        return self.master.first_name

    def get_budged_from(self):
        if self.budged_from < 0:
            return "Договорная"
        else:
            return self.budged_from

    def get_budged_to(self):
        if self.budged_to < 0:
            return "Договорная"
        else:
            return self.budged_to


class TypesOfWork(models.Model):
    card = models.ForeignKey(CardOfObjectForMaster, on_delete=models.CASCADE)
    work = models.CharField('Тип работ', max_length=200, null=True, blank=True, default=None)


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
