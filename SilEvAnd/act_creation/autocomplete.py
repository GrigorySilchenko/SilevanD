from dal import autocomplete
from .models import RegistryModify

class RegistryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = RegistryModify.objects.all()
        if self.q:
            qs = qs.filter(number__icontains=self.q)
        return qs