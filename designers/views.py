import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Designers, PriceList, CardOfObjectForDesigner, Photo
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.shortcuts import render_to_response
from django.http import HttpResponseBadRequest
from django import forms
from django.template import RequestContext
import django_excel as excel
from .forms import DesignerCreationMultiForm, PriceListForm, CardOfObjectForDesignerForm, PhotoForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission


# @permission_required('can_edit_designers')
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
                month = int(datetime.datetime.strptime(form.data['designers-experience'], "%Y-%m").date().month)
                form.data['designers-experience'] = datetime.datetime.strptime(str(years) + "-" + str(month),
                                                                               "%Y-%m").date()
                return self.send_form(form)
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

        return self.send_form(form)

    def form_valid(self, form):
        # Save the designer first, because the price_list needs a designer before it
        # can be saved.
        designer = form['designers'].save()
        price_list = form['price_list'].save(commit=False)
        # card_of_object = form['card_of_object'].save(commit=False)
        price_list.designer = designer
        price_list.save()
        # card_of_object.designer = designer
        # card_of_object.save()
        # three_d_visualisation = CardOfObjectForDesigner(
        #     three_d_visualisation=self.get_form_kwargs().get('files')['three_d_visualisation'])
        # three_d_visualisation.save()
        return super(DesignerCreationView, self).form_valid(form)
        # return redirect(self.get_success_url())

    def send_form(self, form):
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class DesignerCreate(PermissionRequiredMixin, CreateView):
    model = Designers
    fields = '__all__'
    initial = {'experience': datetime.date.today(), }
    permission_required = 'designers.add_designers'

    def get_success_url(self):
        return reverse('designers:price', kwargs={'pk': self.object.id})


class DesignerUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'designers.add_designers'
    model = Designers
    form_class = DesignerCreationMultiForm

    def send_form(self, form):
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.POST._mutable = True
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        try:
            years = int(datetime.datetime.strptime(form.data['designers-experience'], "%Y-%m-%d").date().year)
            month = int(datetime.datetime.strptime(form.data['designers-experience'], "%Y-%m-%d").date().month)
            day = int(datetime.datetime.strptime(form.data['designers-experience'], "%Y-%m-%d").date().day)
            form.data['designers-experience'] = datetime.datetime.strptime(
                str(years) + "-" + str(month) + '-' + str(day), "%Y-%m-%d").date()
            return self.send_form(form)
        except ValueError:
            try:
                years = int(datetime.datetime.strptime(form.data['designers-experience'], "%Y-%m").date().year)
                month = int(datetime.datetime.strptime(form.data['designers-experience'], "%Y-%m").date().month)
                form.data['designers-experience'] = datetime.datetime.strptime(str(years) + "-" + str(month),
                                                                               "%Y-%m").date()
                return self.send_form(form)
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
        return self.send_form(form)

    def get_success_url(self):
        return reverse('designers:price', kwargs={'pk': self.object['designers'].id})

    def get_form_kwargs(self):
        kwargs = super(DesignerUpdate, self).get_form_kwargs()
        kwargs.update(instance={
            'designers': self.object,
            'price_list': self.object.pricelist,
            # 'card_of_object': self.object.cardofobjectfordesigner_set.all,
        })
        return kwargs


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
    #                 ['designers', 'full_design_project', 'supervision', 'decorating_of_premises', 'working_project',
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


class CardOfObjectForDesignerView(CreateView):
    model = CardOfObjectForDesigner
    template_name = 'designers/card_of_object.html'

    def get_context_data(self, **kwargs):
        context = super(CardOfObjectForDesignerView, self).get_context_data(**kwargs)
        context['message'] = "создаёте"
        return context

    def get_form_class(self):
        return CardOfObjectForDesignerForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(CardOfObjectForDesignerView, self).get_form_kwargs(**kwargs)
        if 'data' in kwargs:
            designer = Designers.objects.get(pk=self.kwargs['pk'])
            instance = CardOfObjectForDesigner(designer=designer)
            kwargs.update({'instance': instance})
        return kwargs

    def get_success_url(self):
        return reverse('designers:price', kwargs={'pk': self.kwargs['pk']})

        # def get_queryset(self):
        #     """
        #     Excludes any questions that aren't published yet.
        #     """
        #     return Designers.objects.all()


class CardOfObjectForDesignerEditView(UpdateView):
    model = CardOfObjectForDesigner
    template_name = 'designers/card_of_object.html'

    def get_context_data(self, **kwargs):
        context = super(CardOfObjectForDesignerEditView, self).get_context_data(**kwargs)
        context['message'] = "редактируете"
        return context

    def get_form_class(self):
        return CardOfObjectForDesignerForm

    def get_success_url(self):
        return reverse('designers:price', kwargs={'pk': self.kwargs['designer_id']})


class CardOfObjectForDesignerDeleteView(DeleteView):
    model = CardOfObjectForDesigner
    template_name = 'designers/card_of_object_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(CardOfObjectForDesignerDeleteView, self).get_context_data(**kwargs)
        context['designer'] = self.kwargs
        context['message'] = 'карточку '

        return context

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(CardOfObjectForDesignerDeleteView, self).get_object()
        return obj

    def get_success_url(self):
        return reverse('designers:price', kwargs={'pk': self.kwargs['designer_id']})


class BasicUploadView(CreateView):
    model = Photo
    template_name = 'designers/basic_upload/index.html'

    def get_form_class(self):
        return PhotoForm

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        card_of_object = CardOfObjectForDesigner.objects.all()
        return card_of_object

    def get_context_data(self, **kwargs):
        context = super(BasicUploadView, self).get_context_data(**kwargs)
        context['designer_id'] = self.kwargs['designer_id']
        context['pk'] = self.kwargs['pk']
        return context

    def get_form_kwargs(self, **kwargs):
        kwargs = super(BasicUploadView, self).get_form_kwargs(**kwargs)
        if 'data' in kwargs:
            card_of_object = CardOfObjectForDesigner.objects.get(pk=self.kwargs['pk'])
            instance = CardOfObjectForDesigner(card_of_object=card_of_object)
            kwargs.update({'instance': instance})
        return kwargs

    def get(self, request, *args, **kwargs):
        designer = Designers.objects.get(id=self.kwargs['designer_id'])
        card_of_object = designer.cardofobjectfordesigner_set.get(id=self.kwargs['pk'])
        photos_list = card_of_object.photo_set.all()
        return render(self.request, 'designers/basic_upload/index.html', {'photos': photos_list,
                                                                          'designer': designer,
                                                                          'card_of_object': card_of_object})

    def post(self, request, *args, **kwargs):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class CardUploadView(CreateView):
    model = Photo
    template_name = 'designers/basic_upload/card_of_object.html'

    def get_context_data(self, **kwargs):
        context = super(CardUploadView, self).get_context_data(**kwargs)
        context['message'] = "загружаете"
        context['designer'] = CardOfObjectForDesigner.objects.get(id=self.kwargs['pk']).designer
        return context

    def get_form_class(self):
        return PhotoForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(CardUploadView, self).get_form_kwargs(**kwargs)
        if 'data' in kwargs:
            card_of_object = CardOfObjectForDesigner.objects.get(pk=self.kwargs['pk'])
            instance = Photo(card_of_object=card_of_object)
            kwargs.update({'instance': instance})
        return kwargs

    def get_success_url(self):
        return reverse('designers:card_photo', kwargs={'designer_id': self.kwargs['designer_id'],
                                                       'pk': self.kwargs['pk']})


class CardPhotoView(generic.DetailView):
    model = CardOfObjectForDesigner
    template_name = 'designers/basic_upload/photo_of_card.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CardPhotoView, self).get_context_data(**kwargs)
        # Add in the publisher
        context['designer'] = Designers.objects.get(id=self.kwargs['designer_id'])
        return context

    def get_object(self, queryset=None):
        return CardOfObjectForDesigner.objects.get(id=self.kwargs['pk'])


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
        return from_date.replace(year=from_date.year - years, day=from_date.day - 1)
    except ValueError:
        return from_date.replace(month=from_date.month - 1, day=28,
                                 year=from_date.year - years)


class CardPhotoEditView(UpdateView):
    model = Photo
    template_name = 'designers/basic_upload/card_of_object.html'

    def get_context_data(self, **kwargs):
        context = super(CardPhotoEditView, self).get_context_data(**kwargs)
        context['message'] = "редактируете"
        return context

    def get_form_class(self):
        return PhotoForm

    def get_success_url(self):
        return reverse('designers:card_photo', kwargs={'designer_id': self.kwargs['designer_id'],
                                                       'pk': self.kwargs['card_id']})


class CardPhotoDeleteView(DeleteView):
    model = Photo
    template_name = 'designers/card_of_object_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(CardPhotoDeleteView, self).get_context_data(**kwargs)
        context['card_of_object'] = self.kwargs
        context['message'] = 'фототографию работы'
        return context

    def get_object(self, queryset=None):
        obj = super(CardPhotoDeleteView, self).get_object()
        return obj

    def get_success_url(self):
        return reverse('designers:card_photo', kwargs={'designer_id': self.kwargs['designer_id'],
                                                       'pk': self.kwargs['card_id']})
