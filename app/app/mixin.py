from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import ContextMixin


class IsStuffDispatchMixin(View):
    @method_decorator(user_passes_test(lambda u: u is not None and u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(IsStuffDispatchMixin, self).dispatch(request, *args, **kwargs)


class IsSuperuserDispatchMixin(View):
    @method_decorator(user_passes_test(lambda u: u is not None and u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(IsSuperuserDispatchMixin, self).dispatch(request, *args, **kwargs)


class TitleContextMixin(ContextMixin):
    title = ''

    def get_context_data(self, **kwargs):
        context = super(TitleContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context