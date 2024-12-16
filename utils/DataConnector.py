import pandas as pd
import numpy as np
import pandasql as psql

class DataConnector(object):
    def __init__(self, database_url=None):
        self.demo_data = self._load_demo_data()

    def _load_demo_data(self):
        df = pd.read_csv("./data/odin_aos.csv")
        return df

    def get_review_count(self, filters):
        filtered = self._filter_demo_data(filters)
        
        # 필터링된 데이터가 비어 있는지 확인
        if filtered.empty:
            return 0  # 데이터가 없을 경우 0을 반환하거나 적절한 기본값을 반환

        # 리뷰 수 계산
        review_count = len(filtered)
        return review_count

    def get_avg_rating(self, filters):
        # 필터링된 데이터를 가져옵니다.
        filtered = self._filter_demo_data(filters)
        
        # SQL 쿼리를 사용하여 평균 평점을 계산합니다.
        query = "SELECT AVG(rating) as avg_rating FROM filtered"
        result = psql.sqldf(query, locals())
        
        # 결과에서 평균 평점을 추출합니다.
        avg_rating = result['avg_rating'].iloc[0]
        
        # 평균 평점을 문자열로 변환하고 소수점 두 자리까지 반올림합니다.
        if pd.notnull(avg_rating):  # 평균 평점이 NaN이 아닌 경우
            return f"{avg_rating:.2f}"
        else:
            return "N/A" 

    def get_daily_post_counts(self, filters):
        # 필터링된 데이터를 가져옵니다.
        filtered = self._filter_demo_data(filters)
        
        # 날짜별로 그룹화하여 총 게시글 수 계산
        query = "SELECT date, product_name as game, count(*) as post_count from filtered group by 1,2;"
        result = psql.sqldf(query, locals()) 
        return result

    def get_word_cloudtext(self, filters): 
        # 필터링된 데이터를 가져옵니다.
        filtered = self._filter_demo_data(filters)
        
        # 필터링된 데이터 출력
        print("Filtered Data:")
        print(filtered.head())  # 데이터의 일부를 출력하여 확인
        
        # 텍스트 열이 존재하는지 확인
        if 'text' not in filtered.columns:
            print("Error: 'text' column not found in filtered data.")
            return ""
        
        # 텍스트 열을 하나의 긴 문자열로 결합
        long_text = ' '.join(filtered['text'].dropna())
        
        # 결합된 텍스트 출력
        print("Combined Text:")
        print(long_text[:100])  # 텍스트의 일부를 출력하여 확인
        
        return long_text

    def get_rating_counts(self, filters):   
        # 필터링된 데이터를 가져옵니다.
        filtered = self._filter_demo_data(filters)
        query = "select product_name as game, rating, count(*) as count from filtered group by 1,2 "
        filtered_data = psql.sqldf(query, locals())

        return filtered_data
    
    def get_keyword_data(self, filters, keyword):   
        # 필터링된 데이터를 가져옵니다.
        filtered = self._filter_demo_data(filters)
        
        # SQL 인젝션 방지를 위해 쿼리 파라미터를 안전하게 처리
        query = f"SELECT date, rating, text FROM filtered WHERE text LIKE '%{keyword}%'; "
        filtered_data = psql.sqldf(query, locals())

        return filtered_data
    
    def get_available_languages(self):
        # 'language' 열의 고유 값을 추출하여 정렬된 리스트로 반환
        languages = self.demo_data['language'].dropna().unique()
        return pd.DataFrame({'language': sorted(languages)})
    
    def get_available_countries(self):
        # 'country' 열의 고유 값을 추출하여 정렬된 리스트로 반환
        countries = self.demo_data['country'].dropna().unique()
        return pd.DataFrame({'country': sorted(countries)})

    def get_available_games(self):
            # 'product_id' 열의 고유 값을 추출하여 정렬된 리스트로 반환
        games = self.demo_data['product_name'].dropna().unique()
        return pd.DataFrame({'game': sorted(games)})

    def get_long_text(self,filters):
        # 'product_id' 열의 고유 값을 추출하여 정렬된 리스트로 반환
        filtered = self._filter_demo_data(filters)
        long_text = ' '.join(filtered['text'].dropna())
        return long_text
    
    def get_game_long_text(self, filters):
        # 필터 조건에 맞는 데이터 필터링
        filtered = self._filter_demo_data(filters)
        
        # 각 게임별로 리뷰를 하나의 텍스트로 결합
        game_reviews = filtered.groupby('product_name')['text'].apply(' '.join).reset_index()
        
        # 각 게임의 이름과 리뷰를 결합하고, '/'로 구분하여 하나의 긴 문자열로 결합
        long_text = ' / '.join(game_reviews.apply(lambda row: f"{row['product_name']}: {row['text']}", axis=1))
        
        return long_text

    def get_default_data(self, filters):
        return self._filter_demo_data(filters)[['date',  'text']]

    def _filter_demo_data(self, filters):
        # 날짜 형식 변환
        demo_data = self.demo_data
        # self.demo_data['date'] = pd.to_datetime(self.demo_data['date'])
         # date_filter = (self.demo_data['date'] >= str(start_date) ) & (self.demo_data['date'] <= str(end_date))
        device = filters.get("device", '')  
        start_date = pd.to_datetime(filters.get("start_date", '1900-01-01'))
        end_date = pd.to_datetime(filters.get("end_date", '2100-01-01'))
        keyword = filters.get("keyword", '')  
        rating_min, rating_max = filters.get("rating", [1, 5])
        query = f"select * from demo_data where date >= '{str(start_date)}' and date <= '{str(end_date)}' and rating between {rating_min} and {rating_max} "
        game_filter= filters.get("game", [])
        country_filter = ','.join(filters.get("country", []))
        language_filter = ','.join(filters.get("language", []))
        if len(game_filter)>0: 
            game_condtion = ",".join(f'"{item}"' for item in game_filter)

            query += f" and product_name in ( {game_condtion}) "
        if len(country_filter) > 0:
            query += f" and country in ( '{country_filter}' )"
        if len(language_filter) > 0:
   
            query += f" and language in ( '{language_filter}' )"
        if len(keyword)!= 0 :
            query  += f" and text like '%{keyword}%' )"
        if len(device) != 0 :
            device_condition = ",".join(f'"{item}"' for item in device)
            query  += f" and device in ( {device_condition}) "
        filtered_data = psql.sqldf(query, locals())
        print(query)
        print(len(filtered_data))
        # print(filtered_data)
        return filtered_data

