from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.core import serializers
from django.http import JsonResponse
import json

from .models import Campaign, Contribution, Connection


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
    similar_campaigns = campaign.similar_campaigns()

    return render(
        request, 'fec/campaign.html', {
            'campaign': campaign,
            'committees': committees,
            'contributions': contributions,
            'similar_campaigns': similar_campaigns
        })


def graph(request):
    return render(request, "fec/graph.html")


def graph_campaigns(request):
    campaigns = Campaign.connected_campaigns()
    data = list(campaigns.values())

    return JsonResponse(data, safe=False)

def graph_connections(request):
    connections = Connection.edges()

    return JsonResponse(connections, safe=False)
