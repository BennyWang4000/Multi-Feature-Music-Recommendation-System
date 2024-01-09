# %%
'''
the spotify api have been modified 
change the module code to below

    def get_track_url_info(self, url: str) -> dict:
        # * modified
        # try:
        page_content = self.session.get(
            url=self._turn_url_to_embed(url=url), stream=True).content
        # try:
        bs_instance = BeautifulSoup(page_content, "lxml")
        print(bs_instance)
        url_information = self._str_to_json(
            string=bs_instance.find("script", {"id": "__NEXT_DATA__"}).contents[0])['props']['pageProps']['state']['data']['entity']
        title = url_information['name']
        preview_mp3 = url_information['audioPreview']['url']
        duration = self._ms_to_readable(
            millis=int(url_information['duration']))
        artist_name = url_information['artists'][0]['name']
        artist_url = url_information['artists'][0]['uri']
        # album_title = url_information['album']['name']
        # album_cover_url = url_information['album']['images'][0]['url']
        # album_cover_height = url_information['album']['images'][0]['height']
        # album_cover_width = url_information['album']['images'][0]['width']
        release_date = url_information['releaseDate']
        # total_tracks = url_information['album']['total_tracks']
        # type_ = url_information['album']['type']

        return {
            'title': title,
            'preview_mp3': preview_mp3,
            'duration': duration,
            'artist_name': artist_name,
            'artist_url': artist_url,
            # 'album_title': album_title,
            # 'album_cover_url': album_cover_url,
            # 'album_cover_height': album_cover_height,
            # 'album_cover_width': album_cover_width,
            'release_date': release_date,
            # 'total_tracks': total_tracks,
            # 'type_': type_,
            'ERROR': None,
        }
        #     except Exception as error:
        #         if self.log:
        #             logger.error(error)
        #         try:
        #             bs_instance = BeautifulSoup(page_content, "lxml")
        #             error = bs_instance.find('div', {'class': 'content'}).text
        #             if "Sorry, couldn't find that." in error:
        #                 return {"ERROR": "The provided url doesn't belong to any song on Spotify."}
        #         except Exception as error:
        #             if self.log:
        #                 logger.error(error)
        #             return {"ERROR": "The provided url is malformed."}
        # except:
        #     raise


    def download_preview_mp3(self, url: str, path: str = '', with_cover: bool = False) -> str:
        try:
            page_content = self.session.get(
                url=self._turn_url_to_embed(url=url), stream=True).content
            try:
                bs_instance = BeautifulSoup(page_content, "lxml")
                url_information = self._str_to_json(
                    string=bs_instance.find("script", {"id": "__NEXT_DATA__"}).contents[0])['props']['pageProps']['state']['data']['entity']
                title = url_information['name']
                id = url_information['id']
                # album_title = url_information['album']['name']
                preview_mp3 = url_information['audioPreview']['url']
                album_cover_url = url_information['coverArt']['sources'][0]['url']

                try:
                    return self._preview_mp3_downloader(url=preview_mp3, file_name=title + '-' + id, path=path,
                                                        with_cover=with_cover, cover_url=album_cover_url)
                except Exception as error:
                    if self.log:
                        logger.error(error)
                    return "Couldn't download the cover."
            except:
                try:
                    # bs_instance = BeautifulSoup(page_content, "lxml")
                    # error = bs_instance.find('div', {'class': 'content'}).text
                    # if "Sorry, couldn't find that." in error:
                    return "The provided url doesn't belong to any song on Spotify."
                except Exception as error:
                    if self.log:
                        logger.error(error)
                    raise
        except:
            raise

'''
from SpotifyScraper.scraper import Scraper, Request
from tqdm import tqdm
import pandas as pd
import os

URL = 'https://open.spotify.com/track/'
GENRES_PATH = '/home/wslu/bdm/Big-Data-Mining-Proposal/data/Music genres dataset/csv/songs.csv'
OUTPUT_DIR = '/mnt/e/dataset/spotify_preview_target'

cols = {
    "spotify_id": 0,
    "name": 1,
    "artist": 2,
    "position": 3,
    "genre_name": 4, }
# %%
if __name__ == '__main__':

    ori_df = pd.read_csv(GENRES_PATH, sep=';', header=0)
    blues_df = ori_df[ori_df['genre_name'].str.contains('blues') == True]
    rap_df = ori_df[ori_df['genre_name'].str.contains('trap') == False]
    rap_df = rap_df[rap_df['genre_name'].str.contains('rap') == True]
    blues_df.to_csv(OUTPUT_DIR + '/blues.csv', index=False)
    rap_df.to_csv(OUTPUT_DIR + '/rap.csv', index=False)
    dfs = [rap_df]

    request = Request().request()
    for df in dfs:
        for row in tqdm(df.iterrows(), total=len(df.index)):
            row = row[1]
            file_dir = os.path.join(OUTPUT_DIR, row['genre_name'])
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            path = Scraper(session=request).download_preview_mp3(
                url=URL + row['spotify_id'], path=file_dir)

# %%
# * non-duplicated
blues_df = pd.read_csv(OUTPUT_DIR + '/blues.csv')
rap_df = pd.read_csv(OUTPUT_DIR + '/rap.csv')
blues_df = blues_df.drop(columns=['position', 'genre_name'])
blues_df = blues_df.drop_duplicates()
blues_df.to_csv(OUTPUT_DIR + '/blues_non_duplicated.csv', index=False)
rap_df = rap_df.drop(columns=['position', 'genre_name'])
rap_df = rap_df.drop_duplicates()
rap_df.to_csv(OUTPUT_DIR + '/rap_non_duplicated.csv', index=False)

# %%
