from django.shortcuts import get_object_or_404


class ObjectDetailMixin(object):
    form_class = None
    model = None
    lookup = None
    template_name = None
    context_object_name = None

    def get_object(self, queryset=None):
        if self.lookup == 'slug':
            return get_object_or_404(self.model, url=self.kwargs.get(self.lookup))
        else:
            return get_object_or_404(self.model, pk=self.kwargs.get(self.lookup))

    def get_initial(self):
        initial = super().get_initial()
        initial['content_type'] = self.get_object().get_content_type
        initial['object_id'] = self.get_object().id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['reviews'] = self.get_object().reviews
        return context

