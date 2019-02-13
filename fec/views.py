from django.shortcuts import get_object_or_404, render

from .models import Politician


def index(request):
    politicians = Politician.objects.all()
    return render(request, 'fec/politician_index.html',
                  {'politicians': politicians})


def politician(request, politician_id):
    politician = get_object_or_404(Politician, pk=politician_id)
    campaigns = politician.campaign_set.all()

    return render(request, 'fec/politician.html', {
        'politician': politician,
        'campaigns': campaigns
    })
