import requests
import json
import serpapi
from openai import OpenAI
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import retrive_abstract
import re

# Set up the Google Scholar API endpoint and parameters
base_url = "https://serpapi.com/search.json"
YOUR_API_KEY = "a3210d9144d16801c3abe0ead3c722df14fa68a26b7312a2a69dd098b484dbf4"
openai_api_key = "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"
GOOGLE_API_KEY = "a3210d9144d16801c3abe0ead3c722df14fa68a26b7312a2a69dd098b484dbf4"

def get_user_choice(types):
    types_list = types.split("Cluster")
    types_list = [t.strip() for t in types_list if t.strip()]
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(types):
                return types_list[choice-1]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def cluster_paper(papers):
    titles_abstracts = ""
    for paper in papers:
        titles_abstracts += paper["title"] + " " + paper['abstract'] + "\n"
    #print(titles_abstracts)

    client = OpenAI(
        api_key=openai_api_key,
    )

    prompt = f"Please cluster the following 10 papers into 2-4 types based on their titles and abstracts,\n{titles_abstracts}\n. Return your answers exactly in the format of (each cluster should be in the same line): Cluster 1: (brief summary of the cluster in 15 words); (Don't wrap here)paper number: ...(e.g.: 1,3,7) \n Cluster 2: ...; paper number:...\n Cluster 3: ...; paper number:... "

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    new_types = response.choices[0].message.content
    return new_types

def reconstruct_query(query):
    client = OpenAI(
        api_key=openai_api_key,
    )

    prompt = (f"You are an assistant to help users find paper more easily on Google Scholar, Reconstruct the following query: '{query}'; "
              f"examples!!: user query 'original paper of transformer', reconstruct query 'attention is all you need OR transformer model';"
              f"user query 'original paper of diffusion model', reconstruct query 'Denoising Diffusion Probabilistic Models OR diffusion model'"
              f"[Very Important: If you know the answer of the user query, you should add your answer to the reconstructed query] Some tips on How to reconstruct: 1.You should use boolean operations (of google scholar) like OR, - (Exclude a term from the search), ~ (Synonyms of term), etc); 2.You may replace some terms in the user's query, if you think it's not accurate, with more academical words based on the meaning of the user's query. 3. You should try your best to understand the semantic meaning of the user input '{query}', find the logic, try not use 'AND' .  4. If you know the paper the user want to search for in the '{query}', you can just add the paper title to the reconstruct query. for instance, if the user query is 'original paper of transformer', and you know the original paper of transformer is 'attention is all you need', you should add 'attention is all you need‘ in the reconstructed query. 5. note that google scholar search use keyword matching, thus you should not keep the words that you think will not appear in the target papers, or replace those with academic synonyms."
              f"IMPORTANT: just return the reconstructed version of this query: '{query}'"
              f"!remember the example!! Reconstructed query:")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    reconstructed_query = response.choices[0].message.content
    return reconstructed_query

def get_clusters_func(user_query):
    refined_query = reconstruct_query(user_query)
    print(refined_query)
    papers_lst = retrive_abstract.search_papers(refined_query, GOOGLE_API_KEY)
    cluster_types = cluster_paper(papers_lst)
    print(cluster_types)
    cluster_dict = string_to_dict(cluster_types)


    return papers_lst, cluster_dict


def string_to_dict(string):
    result = {}
    # Adjust the regular expression to handle descriptions ending with a period followed by "paper number" and possible space variations
    pattern = r"Cluster (\d+): (.*?)(?:[.;]|;|\n)(?:\s*paper number: )([\d, ]+)"

    # Use re.DOTALL to allow the dot (.) to match newlines
    matches = re.findall(pattern, string, re.DOTALL)

    for match in matches:
        cluster_name = f"Cluster {match[0]}"
        description = match[1].strip().rstrip('.')  # Remove any trailing period from the description
        paper_numbers = [int(num.strip()) for num in match[2].split(",")]

        result[cluster_name] = {
            "description": description,
            "paper_numbers": paper_numbers
        }

    return result





if __name__ == "__main__":

    # user_query = "img seg for people"
    # papers, clusters = get_clusters_func(user_query)
    # print(papers)
    # print(clusters)
    query = reconstruct_query('original paper of transformer')
    print(query)




    '''
    sample output:
    papers:
    [{'title': 'Recent advance in content-based image retrieval: A literature survey', 'link': 'https://arxiv.org/abs/1706.06064', 'abstract': 'Abstract:The explosive increase and ubiquitous accessibility of visual data on the Web have led to the prosperity of research activity in image search or retrieval. With the ignorance of visual content as a ranking clue, methods with text search techniques for visual retrieval may suffer inconsistency between the text words and visual content. Content-based image retrieval (CBIR), which makes use of the representation of visual content to identify relevant images, has attracted sustained attention in recent two decades. Such a problem is challenging due to the intention gap and the semantic gap problems. Numerous techniques have been developed for content-based image retrieval in the last decade. The purpose of this paper is to categorize and evaluate those algorithms proposed during the period of 2003 to 2016. We conclude with several promising directions for future research.'}, {'title': 'Appion: an integrated, database-driven pipeline to facilitate EM image processing', 'link': 'https://www.sciencedirect.com/science/article/pii/S1047847709000173', 'abstract': '… , inputs, and outputs from every processing step. This consortium of … reconstruction, and querying this information provides insight into the results of varying algorithms and methods …'}, {'title': 'Structure and texture filling-in of missing image blocks in wireless transmission and compression applications', 'link': 'https://ieeexplore.ieee.org/abstract/document/1197835/', 'abstract': '… of the image. Instead of using common retransmission query protocols, we aim to reconstruct the lost … Most schemes reported in the literature deal with image transmission in error-prone …'}, {'title': 'Collective reconstructive embeddings for cross-modal hashing', 'link': 'https://ieeexplore.ieee.org/abstract/document/8594588/', 'abstract': '… literature, … image-query-text and text-query-image tasks are very close for our CRE in all the datasets, which testifies the effectiveness of unified embeddings of Collective Reconstructive …'}, {'title': 'Geometric applications of the split Bregman method: segmentation and surface reconstruction', 'link': 'https://link.springer.com/article/10.1007/s10915-009-9331-z', 'abstract': 'Variational models for image segmentation have many applications, but can be slow to compute. Recently, globally convex segmentation models have been introduced which are very reliable, but contain TV-regularizers, making them difficult to compute. The previously introduced Split Bregman method is a technique for fast minimization of L1 regularized functionals, and has been applied to denoising and compressed sensing problems. By applying the Split Bregman concept to image segmentation problems, we build fast solvers which can out-perform more conventional schemes, such as duality based methods and graph-cuts. The convex segmentation schemes also substantially outperform conventional level set methods, such as the Chan-Vese level set-based segmentation algorithm. We also consider the related problem of surface reconstruction from unorganized data points, which is used for constructing level set representations in 3 dimensions. The primary purpose of this paper is to examine the effectiveness of “Split Bregman” techniques for solving these problems, and to compare this scheme with more conventional methods.'}, {'title': 'Active learning for interactive 3D image segmentation', 'link': 'https://link.springer.com/chapter/10.1007/978-3-642-23626-6_74', 'abstract': 'We propose a novel method for applying active learning strategies to interactive 3D image segmentation. Active learning has been recently introduced to the field of image segmentation. However, so far discussions have focused on 2D images only. Here, we frame interactive 3D image segmentation as a classification problem and incorporate active learning in order to alleviate the user from choosing where to provide interactive input. Specifically, we evaluate a given segmentation by constructing an “uncertainty field” over the image domain based on boundary, regional, smoothness and entropy terms. We then calculate and highlight the plane of maximal uncertainty in a batch query step. The user can proceed to guide the labeling of the data on the query plane, hence actively providing additional training data where the classifier has the least confidence. We validate our method against random plane selection showing an average DSC improvement of 10% in the first five plane suggestions (batch queries). Furthermore, our user study shows that our method saves the user 64% of their time, on average.'}, {'title': 'Fast query for exemplar-based image completion', 'link': 'https://ieeexplore.ieee.org/abstract/document/5482183/', 'abstract': '… Most of the existing methods in literature take quite a long time … reconstruct the highly textured input image – the better the original image is reconstructed, the more accurate the image …'}, {'title': 'Image processing and data analysis: the multiscale approach', 'link': 'https://books.google.com/books?hl=en&lr=&id=yC96XMoABEUC&oi=fnd&pg=PP1&dq=Reconstructed+query:+image+segmentation+techniques+in+academic+literature&ots=dT-TWg0N8L&sig=M3-NeWP6146S9Sm3ss8Pefxcr4M', 'abstract': '… Dr Matthew Freedman, Georgetown University, and our attention … queries may need to be supported, based on an image database. … 1 The reconstruction method is the same as with the …'}, {'title': 'Medical image segmentation in oral-maxillofacial surgery', 'link': 'https://www.sciencedirect.com/science/article/pii/B9780128232996000018', 'abstract': '… matching, where the query image was compared with a large … of mandible reconstruction is the mandible segmentation process… , the publications related to mandible segmentation have …'}, {'title': 'Robust and efficient Fourier–Mellin transform approximations for gray-level image reconstruction and complete invariant description', 'link': 'https://www.sciencedirect.com/science/article/pii/S1077314201909221', 'abstract': '… it was later used in digital signal and image processing [18–20]. … be found in mathematical literature on harmonic analysis (30)… can be compared with any query image and ranked by the …'}]

    
    clusters:
    {'Cluster 1': {'description': 'Content-based image retrieval algorithms', 'paper_numbers': [1]}, 'Cluster 2': {'description': 'Image processing and segmentation techniques', 'paper_numbers': [4, 6, 7]}, 'Cluster 3': {'description': 'Active learning for interactive 3D image segmentation', 'paper_numbers': [5]}}
    '''

    '''
    user_query = 'find cars in img'
    print(reconstruct_query(user_query))
    '''