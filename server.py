from flask import Flask, render_template, request, jsonify, session
import requests
import json
import serpapi
from openai import OpenAI
import query_generation
import requests
import retrive_abstract
import get_clusters

app = Flask(__name__)
app.secret_key = 'your_secret_key'
base_url = "https://serpapi.com/search.json"
YOUR_API_KEY = "a3210d9144d16801c3abe0ead3c722df14fa68a26b7312a2a69dd098b484dbf4"
openai_api_key = "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"
GOOGLE_API_KEY = "a3210d9144d16801c3abe0ead3c722df14fa68a26b7312a2a69dd098b484dbf4"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/results/<int:result_id>', methods=['POST'])
def results(result_id):
    user_query = request.form['query']
    session['papers']= []
    session['user_query'] = user_query
    #session['user_queries']=[]
    #session['user_queries'].append(user_query)
    with open('selected_papers.json', 'w') as f:
        json.dump('', f)
        f.close()

    print("result test")
    print("resultId is",result_id)
    #print(user_query)
    #print(session['user_queries'])
    papers, clusters = get_clusters.get_clusters_func(user_query)
    with open('static/new_papers.json', 'w') as f:
        json.dump(papers, f)
    with open('static/new_clusters.json', 'w') as f:
        json.dump(clusters, f)
    print(papers)
    print(clusters)
    return render_template('results.html', papers=papers, clusters=clusters,result_id = result_id)

@app.route('/next', methods=['POST'])
def next_query():
    data = request.get_json()
    cluster_descriptions = data['clusterDescriptions']
    papers = data['papers']
    print("next test")
    #print("the result id is:",result_id)
    print(cluster_descriptions)
    print(papers)
    user_query = session.get('user_query')  # Retrieve user_query from the session
    session['papers'].extend(papers)
    # Concatenate cluster descriptions with the query to form a new query
    new_query = query_generation.query_merge(user_query, cluster_descriptions)
    session['user_query']   = new_query
    #session['user_queries'].append(new_query)
    print(new_query)

    # Append the papers to the JSON file
    with open('selected_papers.json', 'w') as f:
        json.dump(session['papers'], f)
        f.close()
    # Perform the search with the new query
    new_papers, new_clusters = get_clusters.get_clusters_func(new_query)
    #new_papers = retrive_abstract.search_papers(new_query, GOOGLE_API_KEY)
    with open('static/new_papers.json', 'w') as f:
        json.dump(new_papers, f)
    with open('static/new_clusters.json', 'w') as f:
        json.dump(new_clusters, f)
    print("New papers and clusters")
    print(new_clusters)
    print(new_papers)
    return render_template('results_content.html', papers=new_papers, clusters=new_clusters)

@app.route('/history')
def history():
    with open('selected_papers.json') as file:
        json_data = file.read()
        papers = json.loads(json_data)
    return render_template('history.html', papers=papers)

if __name__ == '__main__':
    app.run(debug=True,port= 5001)