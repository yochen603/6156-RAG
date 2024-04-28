from openai import OpenAI

openai_api_key = "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"
def query_merge(query, description_lst):
    client = OpenAI(
        api_key=openai_api_key,
    )

    # Combine old queries and descriptions into a single string
    old_queries = query
    descriptions = ", ".join(description_lst)

    prompt = f"""
    You are an assistant that helps the user generate a new query suitable for a Google Scholar search.

    Given the following old query:
    {old_queries}

    And the following field descriptions the user want to search for:
    {descriptions}

    Please reconstruct and generate a new query based on the provided information. The new query should use boolean operations of Google Scholar like OR, - (Exclude a term from the search), ~ (Synonyms of term), etc.
    
    The new query you generate should be too strict, Use OR try not use 'AND'. IMPORTANT: You should put more focus on the old query (its semantic meaning) than the descriptions.

    New query:
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    new_query = response.choices[0].message.content
    return new_query

if __name__ == "__main__":
    query_lst = 'closeness of img'
    description_lst = ['Proximity algorithms and image models','Activity-based bioconjugation for proximity-activated imaging reporters']
    new_query = query_merge(query_lst, description_lst)
    print(new_query)
    '''
    example output:
    "Proximity algorithms AND image models OR activity-based bioconjugation -img ~image"
    '''