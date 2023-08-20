from django.http import JsonResponse
from arxiv import Search, SortCriterion, SortOrder
from django.shortcuts import render
from .models import SearchHistory

def search_arxiv(request):
    query_string = request.GET.get('query')
    results = []
    if query_string:
        SearchHistory.objects.create(query=query_string)
    if query_string:
        # Search arXiv and get the results
        search_results = Search(query=query_string, max_results=10, sort_by=SortCriterion.Relevance, sort_order=SortOrder.Descending)

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

from django.db.models import Count
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

@csrf_exempt 
@login_required()
def recommended_papers(request):
    user = request.user
    interested_domains = user.domains.all()  # Assuming "domains" is the related name in the User model
    
    recommended_results = []
    papers = set()
    
    for domain in interested_domains:
        # Search arXiv based on the user's interested domain and get relevant information
        search_results = Search(query=domain.name, max_results=1, sort_by=SortCriterion.LastUpdatedDate, sort_order=SortOrder.Descending)
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
                    'related': domain.name
                })
                papers.add(paper.title)
    
    return JsonResponse(recommended_results, safe=False)

