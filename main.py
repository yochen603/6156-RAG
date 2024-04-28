import requests
import json
import serpapi
from openai import OpenAI
import google.generativeai as genai
import requests
import query_generation
import retrive_abstract
import get_clusters

# Set up the Google Scholar API endpoint and parameters
base_url = "https://serpapi.com/search.json"
YOUR_API_KEY = "7b77fd6eeb8f4a8a60cc6d46f44442cedc428041853ee43b556800dfa8432c15"
openai_api_key = "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"
GOOGLE_API_KEY = "a3210d9144d16801c3abe0ead3c722df14fa68a26b7312a2a69dd098b484dbf4"

def string_to_dict(papers_lst, cluster_dict, user_input):
    selected_clusters = user_input.split(',')
    des_lst = []
    selected_papers_lst = []

    for cluster in selected_clusters:
        cluster_key = f'Cluster {cluster.strip()}'
        if cluster_key in cluster_dict:
            des_lst.append(cluster_dict[cluster_key]['description'])
            paper_indices = cluster_dict[cluster_key]['paper_numbers']
            for index in paper_indices:
                if index - 1 < len(papers_lst):
                    selected_papers_lst.append({
                        'title': papers_lst[index - 1]['title'],
                        'link': papers_lst[index - 1]['link']
                    })
                else:
                    print(f"Warning: Paper number {index} is out of range and will not be included.")
    return des_lst, selected_papers_lst


if __name__ == "__main__":
    Paper_outcome = []
    continue_search = True
    user_query = input("Please enter a query: ")

    while continue_search:
        query = get_clusters.reconstruct_query(user_query)
        papers_lst = retrive_abstract.search_papers(query, YOUR_API_KEY)
        cluster_types = get_clusters.cluster_paper(papers_lst)
        print(cluster_types)
        user_choice = input("Which cluster are you interested in? (example: 1   1,2   2,3,4):")
        cluster_dict = get_clusters.string_to_dict(cluster_types)
        description_list, selected_papers_list = string_to_dict(papers_lst, cluster_dict, user_choice)
        Paper_outcome.extend(selected_papers_list)

        conti = input("Would you like to continue (y/n): ")
        if conti.lower() == "y":
            new_query = query_generation.query_merge(query, description_list)
            user_query = new_query  # Update the user_query to the newly generated query for the next iteration
        else:
            continue_search = False

    print("Final list of selected papers:")
    for paper in Paper_outcome:
        print(f"Title: {paper['title']}")
        print(f"Link: {paper['link']}")
        print()
