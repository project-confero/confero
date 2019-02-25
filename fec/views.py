from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

from .models import Campaign


def index(request):
    search = request.GET.get('search')

    if search:
        all_campaigns = Campaign.objects.filter(name__icontains=search)
    else:
        all_campaigns = Campaign.objects.all()

    # Show 25 campaigns per page
    paginator = Paginator(all_campaigns, 25)

    page = request.GET.get('page')

    campaigns = paginator.get_page(page)

    return render(request, 'fec/campaign_index.html', {'campaigns': campaigns})


def campaign_search(request):
    all_campaigns = Campaign.objects.all()

    # Show 25 campaigns per page
    paginator = Paginator(all_campaigns, 25)

    page = request.GET.get('page')

    campaigns = paginator.get_page(page)

    return render(request, 'fec/campaign_index.html', {'campaigns': campaigns})


def campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id)

    committees = campaign.committee_set.all()

    return render(request, 'fec/campaign.html', {
        'campaign': campaign,
        'committees': committees
    })
