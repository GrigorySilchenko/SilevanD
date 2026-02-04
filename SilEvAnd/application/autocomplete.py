from dal import autocomplete
from .models import Declarant

class DeclarantAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Declarant.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs