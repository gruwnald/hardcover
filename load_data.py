import requests, os
from collections import defaultdict
from time import sleep
import pandas as pd

def api_to_csv(filename: str, batch_size: int = 1000, delay_between_tries: int = 30):
    url = 'https://api.hardcover.app/v1/graphql'
    headers = {
        'Authorization': 'Bearer ' + os.getenv('HARDCOVER_API_KEY'),
        'Content-Type': 'application/json'
    }
    # nth batch on size batch_size of books with more than 10 ratings and more than 3 tags
    query = lambda n: """
      query Books {
        books(
          where: {
            ratings_count: {_gt: 10},
            taggings_aggregate: {count: {predicate: {_gt: 3}}}
            }
          order_by: {id: asc}
          offset: """ + str(n*batch_size) + """
          limit: """ + str(batch_size) + """
        ) {
          id
          title
          rating
          ratings_count
          ratings_distribution
          release_year
          pages
          users_count
          reviews_count
          editions_count
          lists_count
          journals_count
          taggings {
            tag {
              tag
              tag_category {
                category
              }
            }
          }
        }
      }
      """
    books = []
    i = 0
    while len(books) < 11000:
        res = requests.post(url, headers=headers, json={'query': query(i)})

        #API fails sometimes, so we keep trying until proper response is sent
        while res.status_code != 200:
            print(f"received status code {res.status_code}, sleeping {delay_between_tries}s before another try")
            sleep(delay_between_tries)
            res = requests.post(url, headers=headers, json={'query': query(i)})

        res = res.json().get("data", {}).get("books", [])
        if not res: break
        books += res
        print(f"Fetched {len(books)} books")
        i += 1
    
    for book in books:

        # Ratings
        ratings = book.get("ratings_distribution", {})
        book["ratings"] = {r['rating']: r['count'] for r in ratings}
        del book["ratings_distribution"]

        # Categories
        categories = defaultdict(list)
        for tagging in book.get("taggings", []):
            tag = tagging["tag"]["tag"]
            category = tagging["tag"]["tag_category"]["category"]
            categories[category].append(tag)
        book.update(categories)
        del book["taggings"]

    pd.DataFrame(books).convert_dtypes().set_index('id').to_csv(filename)


def csv_to_df(filename):
    data = pd.read_csv(filename).convert_dtypes().set_index('id')
    eval_cols = ['ratings', 'Genre', 'Mood', 'Pace', 'Tag', 'Content Warning', 'Member']
    data[eval_cols] = data[eval_cols].fillna('[]').map(eval)
    return data