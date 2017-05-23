import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Designers, PriceList
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.shortcuts import render_to_response
from django.http import HttpResponseBadRequest
from django import forms
from django.template import RequestContext
import django_excel as excel
from .forms import DesignerCreationMultiForm, PriceListForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission


# @permission_required('can_edit_designer')
# def renew_book_librarian(request, pk):
#     book_inst = get_object_or_404(Designers, id=pk)
#
#     # If this is a POST request then process the Form data
#     if request.method == 'POST':
#
#         # Create a form instance and populate it with data from the request (binding):
#         form = RenewBookForm(request.POST)
#
#         # Check if the form is valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#             book_inst.experience = form.cleaned_data['renewal_date']
#             book_inst.save()
#
#             # redirect to a new URL:
#             return render(request, 'designers/designer_form.html', {'form': form, 'bookinst': book_inst})
#
#     # If this is a GET (or any other method) create the default form.
#     else:
#         proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#         form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })
#
#     return render(request, 'designers/designer_form.html', {'form': form, 'bookinst': book_inst})


data = [
    [1, 2, 3],
    [4, 5, 6]
]


class DesignerCreationView(PermissionRequiredMixin, CreateView):
    permission_required = 'designers.add_designers'
    form_class = DesignerCreationMultiForm
    template_name = 'designers/designer_creation_form.html'

    def get_success_url(self):
        return reverse('designers:main')

    def post(self, request, *args, **kwargs):
        self.object = None
        request.POST._mutable = True
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # price_for_remodeling_form = PriceListForm(self.request.POST)
        # price_for_wall_and_ceiling_form = CardOfObjectForDesignerForm(self.request.POST)
        try:
            years = int(datetime.datetime.strptime(form.data['designers-experience'], "%Y-%m-%d").date().year)
        except ValueError:
            try:
                years = int(datetime.datetime.strptime(form.data['designers-experience'], "%Y-%m").date().year)
            except ValueError:
                try:
                    years = int(form.data['designers-experience'])
                except ValueError:
                    years = -1
        if years > 0:
            if years < 100:
                form.data['designers-experience'] = years_ago(int(form.data['designers-experience']))
            else:
                form.data['designers-experience'] = datetime.datetime.strptime(str(years), "%Y").date()
        request.POST._mutable = False
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Save the designer first, because the price_list needs a designer before it
        # can be saved.
        designer = form['designers'].save()
        price_list = form['price_list'].save(commit=False)
        price_list.designer = designer
        price_list.save()
        return redirect(self.get_success_url())


class DesignerCreate(PermissionRequiredMixin, CreateView):
    model = Designers
    fields = '__all__'
    initial = {'experience': datetime.date.today(), }
    permission_required = 'designers.add_designers'

    def get_success_url(self):
        return reverse('designers:price', kwargs={'pk': self.object.id})


class DesignerUpdate(UpdateView):
    model = Designers
    fields = ['name', 'phone_number', 'email', 'address', 'working_area', 'distance_work', 'experience',
              'website', 'minimal_order', 'description', 'brigade']


class DesignerDelete(PermissionRequiredMixin, DeleteView):
    model = Designers
    permission_required = 'designers.delete_designers'
    success_url = reverse_lazy('designers:main')


class UploadFileForm(forms.Form):
    file = forms.FileField()


class MainView(generic.ListView):
    template_name = 'designers/main.html'
    context_object_name = 'designers'

    form = UploadFileForm

    # def post(self, request):
    #     form = UploadFileForm(self.request.POST,
    #                           self.request.FILES)
    #
    #     def choice_func(row):
    #         q = Designers.objects.filter(slug=row[0])[0]
    #         row[0] = q
    #         return row
    #
    #     if form.is_valid():
    #         latest_question_list = Designers.objects.all
    #         template = loader.get_template('masters/upload_form.html')
    #         context = {
    #             'latest_question_list': latest_question_list,
    #             'form': self.form
    #         }
    #         self.request.FILES['file'].save_book_to_database(
    #             models=[Designers, PriceList],
    #             initializers=[None, choice_func],
    #             mapdicts=[
    #                 ['name', 'phone_number', 'email', 'address', 'working_area', 'distance_work', 'experience',
    #                  'website', 'minimal_order', 'description', 'brigade'],
    #                 ['designer', 'full_design_project', 'supervision', 'decorating_of_premises', 'working_project',
    #                  'three_d_visualization']]
    #         )
    #         return HttpResponse(template.render(context, request))
    #     else:
    #         return HttpResponseBadRequest()
    def post(self, request):
        form = UploadFileForm(self.request.POST,
                              self.request.FILES)
        if form.is_valid():

            designers = Designers.objects.all
            template = loader.get_template('designers/upload_form.html')
            context = {
                'designers': designers,
                'form': self.form
            }
            self.request.FILES['file'].save_to_database(
                model=Designers,
                mapdict=['name', 'phone_number', 'email', 'address', 'working_area', 'distance_work', 'experience',
                         'website', 'minimal_order', 'description', 'brigade'],
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
        return Designers.objects.all()


class PriceView(generic.DetailView):
    model = Designers
    template_name = 'designers/price.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Designers.objects.all()


class CardView(generic.DetailView):
    model = Designers

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Designers.objects.all()


def download(request, file_type):
    sheet = excel.pe.Sheet(data)
    return excel.make_response(sheet, file_type)


def export_data(request, atype):
    if atype == "sheet":
        return excel.make_response_from_a_table(
            Designers, 'xls', file_name="sheet")
    elif atype == "book":
        return excel.make_response_from_tables(
            [Designers, PriceList], 'xls', file_name="book")
    elif atype == "custom":
        designer = Designers.objects.get(distance_work=True)
        query_sets = PriceList.objects.filter(designer=designer)
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


def years_ago(years, from_date=None):
    if from_date is None:
        from_date = datetime.datetime.now().date()
    try:
        return from_date.replace(year=from_date.year - years, day=from_date.day-1)
    except ValueError:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29
        return from_date.replace(month=2, day=28,
                                 year=from_date.year - years)
