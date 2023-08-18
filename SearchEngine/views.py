from arxiv import Search, SortCriterion, SortOrder
from django.http import JsonResponse
from django.shortcuts import render

from .models import SearchHistory


def search_arxiv(request):
    query_string = request.GET.get("query")
    results = []
    if query_string:
        SearchHistory.objects.create(query=query_string)
    if query_string:
        # Search arXiv and get the results
        search_results = Search(
            query=query_string,
            max_results=10,
            sort_by=SortCriterion.Relevance,
            sort_order=SortOrder.Descending,
        )

        # Extract relevant data and build a list of dictionaries
        for result in search_results.results():
            # Extract author names from Author objects
            author_names = [author.name for author in result.authors]

            result_dict = {
                "title": result.title,
                "authors": ", ".join(author_names),
                "abstract": result.summary,
                "arxiv_id": result.entry_id,
                "published_date": result.published,
                "url": result.pdf_url,
            }
            results.append(result_dict)

    return JsonResponse(results, safe=False)


from datetime import datetime

from django.db.models import Count


def recommended_papers(request):
    # Get the top 5 most searched queries
    top_queries = (
        SearchHistory.objects.values("query")
        .annotate(query_count=Count("query"))
        .order_by("-query_count")[:7]
    )

    recommended_results = []
    processed_topics = set()
    papers = set()
    for entry in top_queries:
        query = entry["query"]
        if query in processed_topics:
            continue

        # Search arXiv based on the query and get relevant information
        search_results = Search(
            query=query,
            max_results=1,
            sort_by=SortCriterion.LastUpdatedDate,
            sort_order=SortOrder.Descending,
        )
        search_results_list = list(search_results.results())
        if search_results_list:
            paper = search_results_list[0]
            if paper.title not in papers:
                author_names = [author.name for author in paper.authors]
                recommended_results.append(
                    {
                        "title": paper.title,
                        "authors": ", ".join(author_names),
                        "abstract": paper.summary,
                        "published_date": paper.published,
                        "url": paper.pdf_url,
                        "related": query,
                    }
                )
            papers.add(paper.title)
        processed_topics.add(query)
    return JsonResponse(recommended_results, safe=False)
