# Anime Bot
# Copyright (c) Jonas0o0 2024
# 
# This software is licensed under the Anime Bot License.
# You may use, modify, and distribute this software under the terms of the Anime Bot License.
# See the LICENSE file for more details.

import aiohttp
from config import *

class jikanRequests():
    def __init__(self) -> None:
        pass

    async def get_url(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['data']
                else:
                    return " "

    async def get_info(self, data):
        i = data
        tittle = i['title']
        url = i["url"]
        img = i['images']['jpg']['image_url']
        episode = i['episodes']
        status = i['status']
        diffuse = i['aired']['string']
        synopsis = i['synopsis']
        try:
            synopsis = synopsis.split('\n')
            synopsis = synopsis[0]
        except:
            synopsis = synopsis
        rank = i['rank']
        if synopsis == None:
            synopsis="None"
        if len(synopsis) > 1023:
            synopsis = str(synopsis)[:1023]

        producers = i.get("producers")
        if producers is not None:
            if i["producers"] != []:
                producers = i["producers"][0]["name"]
            else:
                producers = "Unknow"
        else:
            producers = "Unknow"

        licensors = i.get("licensors")
        if licensors is not None:
            if i["licensors"] != []:
                licensors = i["licensors"][0]["name"]
            else:
                licensors = "Unknow"
        else:
            licensors = "Unknow"

        studios = i.get("studios")
        if studios is not None:
            if i["studios"] != []:
                studios = i["studios"][0]["name"]
            else:
                studios = "Unknow"
        else:
            studios = "Unknow"
        genres = i['genres']
        str_genre = ""
        for o in genres:
            str_genre += o['name'] + ", "
        all_genre = str_genre[:len(str_genre) - 2]

        dico = {'img': img, 'url': url, "title": tittle, "episodes": episode,
                "status": status, "diffuse": diffuse,
                "synopsis": synopsis, "producers": producers, "licensors": licensors,
                "studios": studios, "genres": all_genre, "rank": rank}
        return dico
    
    async def get_anime_by_genre(self, genre, genre2, genre3, type):
        id1 = GENRE_ID[genre]
        if genre2 == None and genre3 == None:
            url = f"https://api.jikan.moe/v4/anime?q=&order_by={type}&genres={id1}"
            data = await self.get_url(url)
            return await self.get_info(data[0])
        if genre2 == None and genre3 != None:
            id3 = GENRE_ID[genre3]
            url = f"https://api.jikan.moe/v4/anime?q=&order_by={type}&genres={id1}&genres={id3}"
            data = await self.get_url(url)
            return await self.get_info(data[0])
        if genre2 != None and genre3 == None:
            id2 = GENRE_ID[genre2]
            url = f"https://api.jikan.moe/v4/anime?q=&order_by={type}&genres={id1}&genres={id2}"
            data = await self.get_url(url)
            return await self.get_info(data[0])
        else:
            id2 = GENRE_ID[genre2]
            id3 = GENRE_ID[genre3]
            url = f"https://api.jikan.moe/v4/anime?q=&order_by={type}&genres={id1}&genres={id2}&genres={id3}"
            data = await self.get_url(url)
            return await self.get_info(data[0])

    async def get_anime_populaire(self):
        url = f"https://api.jikan.moe/v4/top/anime?bypopularity"
        data = await self.get_url(url)
        liste = []
        for i in data:
            url = i['url']
            img = i["images"]["jpg"]['image_url']
            tittle = i['title']
            episode = i['episodes']
            genre = i['genres']
            status = i['status']
            rank = i['rank']
            str_genre = ""
            for o in genre:
                str_genre += o['name']+", "
            all_genre = str_genre[:len(str_genre)-2]
            dico = {'img': img, 'url': url, "title": tittle, "genres": all_genre, "episodes": episode, "status" : status, "rank" : rank}
            liste.append(dico)
        return liste

    async def get_anime(self, id):
        url = f"https://api.jikan.moe/v4/anime/{id}"
        data = await self.get_url(url)
        return await self.get_info(data)

    async def get_anime_advice(self):
        url = f"https://api.jikan.moe/v4/anime/1/recommendations"
        data = await self.get_url(url)
        liste = []
        for i in range(2):
            id = data[i]['entry']['mal_id']
            anime = await self.get_anime(id)
            liste.append(anime)
        return liste

    async def get_anime_random(self):
        url = f"https://api.jikan.moe/v4/random/anime"
        data = await self.get_url(url)
        return await self.get_info(data)

    async def get_anime_by_name(self, name):
        url = f"https://api.jikan.moe/v4/anime?q={name}"
        data = await self.get_url(url)
        if type(data) == list:
            return await self.get_info(data[0])
        else:
            return "Anime not found"
        
    async def get_scheduls(self, day):
        url = "https://api.jikan.moe/v4/schedules?filter="+day
        data = await self.get_url(url)
        liste = []
        for i in data:
            url = i['url']
            img = i["images"]["jpg"]['image_url']
            tittle = i['title']
            episode = i['episodes']
            genre = i['genres']
            status = i['status']
            rank = i['rank']
            str_genre = ""
            for o in genre:
                str_genre += o['name']+", "
            all_genre = str_genre[:len(str_genre)-2]
            dico = {'img': img, 'url': url, "title": tittle, "genres": all_genre, "episodes": episode, "status" : status, "rank" : rank}
            liste.append(dico)
        return liste