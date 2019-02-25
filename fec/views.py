from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

from .models import Campaign, Contribution


def index(request):
    search = request.GET.get('search')

    if search:
        all_campaigns = Campaign.search(search)
    else:
        all_campaigns = Campaign.objects.all()

    # Paginate the campaigns
    paginator = Paginator(all_campaigns, 25)
    page = request.GET.get('page')
    campaigns = paginator.get_page(page)

    return render(request, 'fec/campaign_index.html', {
        'campaigns': campaigns,
        'search': search or ''
    })


def campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id)

    committees = campaign.committee_set.all()
    contributions = Contribution.for_campaign(campaign)

    return render(
        request, 'fec/campaign.html', {
            'campaign': campaign,
            'committees': committees,
            'contributions': contributions
        })
