import datetime

import django_excel as excel
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from masters.forms import PriceForRemodelingFormSet, PriceForWallsAndCeilingFormSet, MasterForm, MasterEditMultiForm
from .forms import MasterCreationMultiForm, PriceForRemodelingForm, PriceForWallsAndCeilingForm
from .models import Question, Choice, Master, PriceForRemodeling, PriceForWallsAndCeiling


class UploadFileForm(forms.Form):
    file = forms.FileField()


class IndexView(generic.ListView):
    template_name = 'masters/upload_form.html'
    context_object_name = 'latest_question_list'
    form = UploadFileForm()

    def post(self, request):
        form = UploadFileForm(self.request.POST,
                              self.request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row

        if form.is_valid():
            latest_question_list = Question.objects.order_by('-pub_date')
            template = loader.get_template('masters/upload_form.html')
            context = {
                'latest_question_list': latest_question_list,
                'form': self.form
            }
            self.request.FILES['file'].save_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[
                    ['question_text', 'pub_date', 'slug'],
                    ['question', 'choice_text', 'votes']]
            )
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseBadRequest()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IndexView, self).get_context_data(**kwargs)
        # Add in the publisher
        context['form'] = self.form
        return context

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'masters/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'masters/results.html'


class MainView(generic.ListView):
    # model = Master
    template_name = 'masters/main.html'
    context_object_name = 'masters'

    form = UploadFileForm

    def post(self, request):
        form = UploadFileForm(self.request.POST,
                              self.request.FILES)

        def choice_func(row):
            q = Master.objects.filter(slug=row[0])[0]
            row[0] = q
            return row

        if form.is_valid():

            masters = Master.objects.all
            template = loader.get_template('masters/upload_masters.html')
            context = {
                'masters': masters,
                'form': self.form
            }
            # ['master_id', 'overhaul', 'party_remodeling', 'remodeling'],

            self.request.FILES['file'].save_to_database(
                model=Master,
                mapdict=['first_name', 'second_name', 'middle_name', 'phone_number', 'email', 'city',
                         'country', 'experience', 'additional_info']
            )
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseBadRequest()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MainView, self).get_context_data(**kwargs)
        # Add in the publisher
        context['form'] = self.form
        return context

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Master.objects.all()


class PriceView(generic.DetailView):
    model = Master
    template_name = 'masters/price.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Master.objects.all()


class MasterCreate(CreateView):
    model = Master
    form_class = MasterForm
    # fields = '__all__'
    initial = {'experience': datetime.date.today(), }

    def get_context_data(self, **kwargs):
        context = super(MasterCreate, self).get_context_data(**kwargs)
        context['price_for_remodeling'] = PriceForRemodeling.objects.all()
        context['price_for_walls_and_ceiling'] = PriceForWallsAndCeiling.objects.all()
        return context

    def get_success_url(self):
        return reverse('masters:price', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        price_for_remodeling_form = PriceForRemodelingForm
        price_for_wall_and_ceiling_form = PriceForWallsAndCeilingForm
        return self.render_to_response(
            self.get_context_data(form=form,
                                  price_for_remodeling_form=price_for_remodeling_form,
                                  price_for_wall_and_ceiling_form=price_for_wall_and_ceiling_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        request.POST._mutable = True
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        price_for_remodeling_form = PriceForRemodelingForm(self.request.POST)
        price_for_wall_and_ceiling_form = PriceForWallsAndCeilingForm(self.request.POST)
        if (form.is_valid() and price_for_remodeling_form.is_valid() and
                price_for_wall_and_ceiling_form.is_valid()):
            return self.form_valid(form, price_for_remodeling_form, price_for_wall_and_ceiling_form)
        else:
            return self.form_invalid(form, price_for_remodeling_form, price_for_wall_and_ceiling_form)

    def form_valid(self, form, price_for_remodeling_form, price_for_wall_and_ceiling_form):
        self.object = form.save()
        price_for_remodeling_form.instance = self.object
        price_for_remodeling_form.save()
        price_for_wall_and_ceiling_form.instance = self.object
        price_for_wall_and_ceiling_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, price_for_remodeling_form, price_for_wall_and_ceiling_form):
        # try:
        # int_to_date = years_ago(int(form.data['experience']))
        # form.data['experience'] = int_to_date
        # self.object = form.save()
        # price_for_remodeling_form.instance = self.object
        # price_for_remodeling_form.save()
        # price_for_wall_and_ceiling_form.instance = self.object
        # price_for_wall_and_ceiling_form.save()
        # return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form,
                                  price_for_remodeling_form=price_for_remodeling_form,
                                  price_for_wall_and_ceiling_form=price_for_wall_and_ceiling_form))


class MasterUpdate(UpdateView):
    model = Master
    form_class = MasterEditMultiForm

    # success_url = reverse_lazy('masters:main')

    def get_success_url(self):
        return reverse('masters:price', kwargs={'pk': self.object['master'].id})

    # fields = ['first_name', 'second_name', 'middle_name', 'phone_number', 'email', 'city', 'country', 'experience',
    #           'additional_info']
    # fields = '__all__'

    def get_form_kwargs(self):
        kwargs = super(MasterUpdate, self).get_form_kwargs()
        kwargs.update(instance={
            'master': self.object,
            'price_for_remodeling': self.object.priceforremodeling,
            'price_for_walls_and_ceiling': self.object.priceforwallsandceiling,
        })
        return kwargs


class MasterDelete(DeleteView):
    model = Master
    success_url = reverse_lazy('masters:main')


class MasterCreationView(PermissionRequiredMixin, CreateView):
    permission_required = 'masters.add_master'
    form_class = MasterCreationMultiForm
    # success_url = reverse_lazy('home')
    template_name = 'masters/master_creation_form.html'

    def get_success_url(self):
        return reverse('masters:main')

    def post(self, request, *args, **kwargs):
        self.object = None
        request.POST._mutable = True
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        try:
            years = int(datetime.datetime.strptime(form.data['master-experience'], "%Y-%m-%d").date().year)
        except ValueError:
            try:
                years = int(datetime.datetime.strptime(form.data['master-experience'], "%Y-%m").date().year)
            except ValueError:
                try:
                    years = int(form.data['master-experience'])
                except ValueError:
                    years = -1
        if years > 0:
            if years < 100:
                form.data['master-experience'] = years_ago(int(form.data['master-experience']))
            else:
                form.data['master-experience'] = datetime.datetime.strptime(str(years), "%Y").date()
        request.POST._mutable = False
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Save the master first, because the price_for_remodeling needs a master before it
        # can be saved.
        master = form['master'].save()
        price_for_remodeling = form['price_for_remodeling'].save(commit=False)
        price_for_remodeling.master = master
        price_for_remodeling.save()
        price_for_walls_and_ceiling = form['price_for_walls_and_ceiling'].save(commit=False)
        price_for_walls_and_ceiling.master = master
        price_for_walls_and_ceiling.save()
        price_for_tiling = form['price_for_tiling'].save(commit=False)
        price_for_tiling.master = master
        price_for_tiling.save()
        return redirect(self.get_success_url())


def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv",
                                       file_name="download")
    else:
        form = UploadFileForm()
    return render(
        request,
        'masters/upload_form.html',
        {
            'form': form,
            'title': 'Excel file upload and download example',
            'header': ('Please choose any excel file ' +
                       'from your cloned repository:')
        })


def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row

        if form.is_valid():
            latest_question_list = Question.objects.order_by('-pub_date')[:5]
            template = loader.get_template('masters/index.html')
            context = {
                'latest_question_list': latest_question_list,
            }
            request.FILES['file'].save_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[
                    ['question_text', 'pub_date', 'slug'],
                    ['question', 'choice_text', 'votes']]
            )
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'masters/upload_form.html',
        {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        })


def export_data(request, atype):
    if atype == "sheet":
        return excel.make_response_from_a_table(
            Master, 'xls', file_name="sheet")
    elif atype == "book":
        return excel.make_response_from_tables(
            [Master, PriceForRemodeling], 'xls', file_name="book")
    elif atype == "custom":
        master = Master.objects.get(experience__lte=datetime.date(2015, 1, 31))
        query_sets = PriceForRemodeling.objects.filter(master=master)
        column_names = ['supervision', 'full_design_project', ]
        return excel.make_response_from_query_sets(
            query_sets,
            column_names,
            'xls',
            file_name="custom"
        )
    else:
        return HttpResponseBadRequest(
            "Bad request. please put one of these " +
            "in your url suffix: sheet, book or custom")


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'masters/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('masters:results', args=(question.id,)))


def years_ago(years, from_date=None):
    if from_date is None:
        from_date = datetime.datetime.now().date()
    try:
        return from_date.replace(year=from_date.year - years, day=from_date.day - 1)
    except ValueError:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29
        return from_date.replace(month=2, day=28,
                                 year=from_date.year - years)
