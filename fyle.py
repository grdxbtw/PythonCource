from email.quoprimime import header_check
from pprint import pprint
from collections import defaultdict
from collections import namedtuple
from datetime import datetime, timedelta
import requests
import csv


class Movie_data:
    def __init__(self, pages_numb):
        self.pages = int(pages_numb)
        self.url = 'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={}'
        self.films_data = []
        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNTUyMjRjYzRlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMDFmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8"
        }
        self.fetch_data()

    def fetch_data(self):
        for page in range(1, self.pages + 1):
            url = self.url.format(page)
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                self.films_data.extend(response.json()['results'])

    def show_keys(self):
        response = requests.get(self.url.format(1), headers=self.headers)
        if response.status_code == 200:
            keys_from_url = response.json()
        return keys_from_url.keys()

    def give_all_data(self):
        return self.films_data

    def give_data_from_pages(self, pages):
        return self.films_data[:pages]

    def give_films_by_index(self, start, end, step):
        return self.films_data[start:end:step]

    def give_most_popular_film(self):
        return max(self.films_data, key=lambda film: film['popularity'])['title']

    def give_movie_by_keywords(self, keywords):
        titles_names = []
        for movie in self.films_data:
            if any(keywords in movie['overview'] for keyword in keywords):
                titles_names.append(movie['title'])
        return titles_names

    def give_unique_genres(self):
        genres = set()
        for movie in self.films_data:
            genres.update(movie['genre_ids'])
        return frozenset(genres)

    def delete_movie_by_genre_id(self, genre_id):
        counter = -1
        for movie in self.films_data:
            counter += 1
            if genre_id in movie['genre_ids']:
                self.films_data.pop(counter)
        return 'movies deleted'

    def collection_grouped_by_genres(self):
        genres = defaultdict(list)
        for movie in self.films_data:
            for genre_id in movie['genre_ids']:
                genres[genre_id].append(movie['title'])
        return genres

    def replaced_films(self):
        copyed_data = self.films_data.copy()
        for movie in self.films_data:
            if movie['genre_ids']:
                movie['genre_ids'][0] = 22
        return copyed_data, self.films_data

    def collection_of_structures(self):
        pairs = []
        for movie in self.films_data:
            title = movie['title']
            popularity = round(movie['popularity'], 1)
            score = int(movie['vote_average'])
            f_date = datetime.strptime(movie['release_date'], '%Y-%m-%d')
            last_day_in_cinema = f_date + timedelta(weeks=14)

            pairs.append({
                'Title': title,
                'Popularity': popularity,
                'Score': score,
                'Last_day_in_cinema': last_day_in_cinema.strftime('%Y-%m-%d')
            })

        pairs.sort(key=lambda movie: (movie['Score'], movie['Popularity']), reverse=True)
        return pairs

    def write_to_file(self, pairs, filepath):
        if str(filepath).lower().endswith('.csv'):
            with open(filepath, 'w', newline='') as file:
                fieldnames = ['Title', 'Popularity', 'Score', 'Last_day_in_cinema']
                csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
                csv_writer.writeheader()
                csv_writer.writerow(pairs)



exemplar_f = Movie_data(3)

# exemplar_f.delete_movie_by_genre_id(28)
pair = exemplar_f.collection_of_structures()
exemplar_f.write_to_file(pair[0], 'cwecm.csv')
# pprint(exemplar_f.show_keys())
pprint(exemplar_f.give_all_data())
# pprint(exemplar_f.collection_of_structures())
# pprint(exemplar_f.replaced_films())
# pprint(exemplar_f.collection_grouped_by_genres())
# pprint(exemplar_f.give_most_popular_film())
# pprint(exemplar_f.give_data_from_pages(3))
# pprint(exemplar_f.give_movie_by_keywords("in the m"))
# pprint(exemplar_f.give_unique_genres())

# url = 'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page= 5'
# headers = {
#     "accept": "application/json",
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNTUyMjRjYzRlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMDFmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8"
# }

