from django.apps import apps
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views import View


class AdminSingleDeleteView(View):
    def get(self, request, *args, **kwargs):
        model = None
        object_id_list = None
        object_list = []
        if request.GET.get('next') is None:
            raise KeyError(str(_("key next must be included in request")))

        if kwargs.get('pk', None):
            object_id_list = kwargs['pk'].split(',')
            model = apps.get_model(kwargs['app_label'], kwargs['model'])
        for object_id in object_id_list:
            object_list.append(model.objects.get(id=int(object_id)))
        return render(request, 'softdelete/delete_confirmation.html', {
            'content': object_list,
            'next': request.GET.get('next'),
        })

    def post(self, request, *args, **kwargs):
        model = None
        object_id_list = None
        if kwargs.get('pk', None):
            object_id_list = kwargs['pk'].split(',')
            model = apps.get_model(kwargs['app_label'], kwargs['model'])
        model.objects.filter(pk__in=object_id_list).delete()
        return redirect(request.GET.get('next'))