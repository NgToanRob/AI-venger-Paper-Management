from django.db.models import Count
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from arxiv import Search, SortCriterion, SortOrder
from django.shortcuts import render
from .models import SearchHistory

@csrf_exempt
def search_arxiv(request):
    query_string = request.GET.get('query')
    results = []


    if request.user.is_authenticated:  # Check if user is logged in
        if query_string:
            SearchHistory.objects.create(query=query_string)
        if query_string:
            # Search arXiv and get the results
            search_results = Search(query=query_string, max_results=10,
                                    sort_by=SortCriterion.Relevance, sort_order=SortOrder.Descending)

            # Extract relevant data and build a list of dictionaries
            for result in search_results.results():
                # Extract author names from Author objects
                author_names = [author.name for author in result.authors]

                result_dict = {
                    'title': result.title,
                    'authors': ', '.join(author_names),
                    'abstract': result.summary,
                    'arxiv_id': result.entry_id,
                    'published_date': result.published,
                    'url': result.pdf_url
                }
                results.append(result_dict)

        return JsonResponse(results, safe=False)
    else:
        return JsonResponse({'message': 'Unauthorized'}, status=401)


@csrf_exempt
def recommended_papers(request):
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({'message': 'Unauthorized'}, status=401)

    interested_topics = user.topics.all()  # Assuming "topics" is a related name in the User model

    recommended_results = []
    papers = set()

    for topic in interested_topics:
        # Search arXiv based on the user's interested domain and get relevant information
        search_results = Search(
            query=topic.name, max_results=1, sort_by=SortCriterion.LastUpdatedDate, sort_order=SortOrder.Descending)
        search_results_list = list(search_results.results())

        for paper in search_results_list:
            if paper.title not in papers:
                author_names = [author.name for author in paper.authors]
                recommended_results.append({
                    'title': paper.title,
                    'authors': ', '.join(author_names),
                    'abstract': paper.summary,
                    'published_date': paper.published,
                    'url': paper.pdf_url,
                    'related': topic.name
                })
                papers.add(paper.title)

    return JsonResponse(recommended_results, safe=False)
