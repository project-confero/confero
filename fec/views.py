from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Candidate, Connection


def index(request):
    search = request.GET.get('search')

    if search:
        all_candidates = Candidate.search(search)
    else:
        all_candidates = Candidate.objects.all()

    # Paginate the candidates
    paginator = Paginator(all_candidates, 25)
    page = request.GET.get('page')
    candidates = paginator.get_page(page)

    return render(request, 'fec/candidate_index.html', {
        'candidates': candidates,
        'search': search or ''
    })


def candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    similar_candidates = candidate.similar_candidates()

    return render(request, 'fec/candidate.html', {
        'candidate': candidate,
        'similar_candidates': similar_candidates
    })


def graph(request):
    return render(request, "fec/graph.html")


def graph_candidates(request):
    candidates = Candidate.connected_candidates()
    data = list(candidates.values())

    return JsonResponse(data, safe=False)


def graph_connections(request):
    connections = Connection.edges()

    return JsonResponse(connections, safe=False)
