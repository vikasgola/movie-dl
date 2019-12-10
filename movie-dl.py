import requests
import re
import os
import random
import wget
import argparse
from bs4 import BeautifulSoup
from terminaltables import AsciiTable

dirpath = os.getcwd()

def urlify(in_string):
    return "%20".join(in_string.split())

def downloadfromLink(url, name=None):
    try:
        dheaders = None
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        session = requests.Session()
        response = session.get(url, headers=headers)
        try:
            cookie = {'Cookie': response.headers['Set-Cookie']}
            headers.update(cookie)
            response = session.post(url, headers=headers)
        except:
            pass

        dllinks0 = re.findall("https?://[a-zA-Z0-9._]+.[a-zA-Z0-9._]+/[a-zA-Z0-9@;:%._\+~#=?&!$^*()\-\[\]/ ]+.mp4", str(response.content))
        dllinks1 = re.findall("https://[a-zA-Z0-9._]+.googleusercontent.com/[-a-zA-Z0-9@:%._\+~#=?&!$^*()-\[\]]+", str(response.content))
        dllinks2 = re.findall("vidnode.net/streaming.php[-a-zA-Z0-9@:%._\+~#=\?&!$^*()\-\[\]]+", str(response.content))
        dllinks3 = re.findall("/getlink.php\?f=https://[a-zA-Z0-9._]+.azmovie.to/[-a-zA-Z0-9@:%._\+~#=?&!$^*()\-\[\]]+", str(response.content))
        # dllinks4 = re.findall("https://fmovies.space/[a-zA-Z0-9@:%._\+~#=?&!$^*()\-\[\] ]+", str(response.content))
        # dllinks5 = re.findall("https://jawcloud.co/[a-zA-Z0-9@;:%._\+~#=?&!$^*()\-\[\]/ ]+", str(response.content))
        dllinks6 = re.findall("https://www.okhatrimaza.art/file/[a-zA-Z0-9@;:%._\+~#=?&!$^*()\-\[\]/ ]+", str(response.content))
        dllinks7 = re.findall("https://spaceshut.website/[a-zA-Z0-9@;:%._\+~#=?&!$^*()\-\[\]/ ]+", str(response.content))
        dllinks7 += re.findall("https://freemoviewap2019.in/[a-zA-Z0-9@;:%._\+~#=?&!$^*()\-\[\]/ ]+", str(response.content))

        if len(dllinks0) +len(dllinks1) + len(dllinks2) + len(dllinks3) + len(dllinks6)  + len(dllinks7) == 0:
            print("Can't Download. Could not found video.")
            exit()
        
        if len(dllinks2) >= 1:
            response = session.get("https://"+dllinks2[0])
            dllinks2 = re.findall("https://vidnode.net/download[a-zA-Z0-9@:%._\+~#=?&!$^*()\-\[\] ]+", str(response.content))
            response = session.get(dllinks2[0])
            dllinks2 = re.findall("https://[a-zA-Z0-9._]+.cdnfile.info/[a-zA-Z0-9@:%._\+~#=?&!$^*()/\-\[\] ;]+", str(response.content))
            dllinks2 = [line.replace('&amp;', '&') for line in dllinks2]
            dllink = dllinks2[len(dllinks2) - 1]
            dllink = urlify(dllink)
        elif len(dllinks3) >= 1:
            dllink = "https://azm.to/" + dllinks3[len(dllinks3) - 1]
            response = session.get(dllink, headers=headers)
            print("Work in Progress!!!")
            exit()
            dllinks3 = re.findall("https://[a-zA-Z0-9._]+.azmovie.to/[-a-zA-Z0-9@:%._\+~#=?&!$^*()\-\[\]]+", str(response.content))
            dllink = dllinks3[len(dllinks3) - 1]
        elif len(dllinks6) >= 1:
            dllink = dllinks6[len(dllinks6) - 1]
            response = session.get(dllink)
            dllinks6 = re.findall("https://www.okhatrimaza.art/server/[a-zA-Z0-9@;:%._\+~#=?&!$^*()\-\[\]/ ]+", str(response.content))
            
            dllink = dllinks6[len(dllinks6) - 1]
            response = session.get(dllink,  headers=headers)
            
            dllinks6 = re.findall("https://www.okhatrimaza.art/download/[a-zA-Z0-9@;:%._\+~#=?&!$^*()\-\[\]/ ]+", str(response.content))
            
            referer = {
                "Referer": dllink,
            }
            headers.update(referer)
            dllink = dllinks6[len(dllinks6) - 1]
            dheaders = tuple(headers.items())
        elif len(dllinks7) >= 1:
            dllink = dllinks7[len(dllinks7) - 1]
            while(".mp4" != dllink[-4:]):
                response = session.get(dllink, headers=headers)
                dllinks7 = re.findall("https://spaceshut.website/[a-zA-Z0-9@;:%._\+~#=?&!$^*()\-\[\]/ ]+", str(response.content))
                dllinks7 += re.findall("https?://[a-zA-Z0-9._]+.[a-zA-Z0-9._]+/[a-zA-Z0-9@;:%._\+~#=?&!$^*()\-\[\]/ ]+.mp4", str(response.content))
                dllink = dllinks7[len(dllinks7) - 1]
        elif len(dllinks1) >= 1:
            dllink = dllinks1[len(dllinks1) - 1]
        else:
            dllink = dllinks0[len(dllinks0) - 1]

        if wget.detect_filename(dllink):
            name = wget.detect_filename(dllink)
        elif name == None:
            name = 'movie-' + str(random.randint(1, 100000))
        path = dirpath + '/' + name

        if name:
            print("Downloading: ", name)
        wget.download(dllink, path, headers=dheaders)
        print("\nFinished!!!")
    except Exception as exception:
        print("Error:", exception.__class__.__name__)
        print("Can't Download. Something goes wrong.")

def searchMovies(name):
    shows = [['ID' ,'Name', 'Year', 'Rating', 'Type']]
    shows_links = []

    # , "https://fmovies.space/search/"+name, "https://fmovies.video/list/"+name
    searchurls = ["https://openloadmovies.uk/?s=" + name, "https://vidnode.net/search.html?keyword=" + name, "https://www.okhatrimaza.art/mobile/search?find=" + name + "&per_page=1", "http://freemoviewap.website/search23.php?search="+name+"&submit=Search", "http://bollywoodfilma.site/"]
    # searchurls = ["http://bollywoodfilma.site/"]
    try:
        responses = [requests.get(searchurl) for searchurl in searchurls]

        content = ""
        for response in responses:
            content += str(response.content)

        webpage = BeautifulSoup(content, 'html.parser')

        articles = webpage.find_all(True, {"class":['result-item', 'video-block', 'ml-item', 'movie-preview', 'prasun']})
        articles2 = webpage.find_all(True, {"class":['w3_agile_featured_movies']})
        if len(articles2) >= 1:
            articles2a = articles2[0].select(".w3l-movie-gride-agile")
            for a in articles2a:
                if name in str.lower(a.text):
                    articles.append(a)
            articles2b = articles2[0].select("p")[:-1]
            articles += articles2b

        id = 1
        for article in articles:
            name_ele = article.select(".title a")
            name_ele += article.select(".fileName")
            name_ele += article.select(".movie-title a")
            name_ele += article.select("span h2")
            name_ele += article.select(".name")
            name_ele += article.select("a b")
            name_ele += article.select(".w3l-movie-text a")
            name = name_ele[0].get_text()
            name = re.sub(r"\\n", "",  name)
            name = name.strip()

            rating_ele = article.select(".rating")
            if len(rating_ele) == 1:
                rating = rating_ele[0].get_text()
            else:
                rating = None
            
            year_ele = article.select(".year")
            year_ele += article.select(".date")
            if len(year_ele) >= 1:
                year = year_ele[0].get_text()[:4]
            else:
                year = None

            link_ele = article.select(".title a")
            link_ele += article.select(".movie-title a")
            link_ele += article.select("a")
            link = link_ele[0]['href']
            link = re.sub(r"\\\"", "",  link)
            link = re.sub(r"\\\'", "",  link)
            if link[:4] != "http":
                if "fmovies.space" in str(article):
                    link = "https://fmovies.space/" + link
                else:
                    link = "https://vidnode.net/" + link
            shows_links.append(link)
            
            ismovie_ele = article.select(".movies")
            if len(ismovie_ele) == 1:
                types = 'Movie'
            elif len(article.select(".tvshows")) == 1:
                types = 'TVShow'
            else:
                if "Season" in name or "Episode" in name:
                    types = 'Series'                
                else:
                    types = None

            shows.append([id, name, year, rating, types])
            id += 1

        showstable = AsciiTable(shows)
        print(showstable.table)

        if len(shows) > 1:
            id = int(input("Download ID?: "))
            if id < len(shows):
                if shows[id][4] == 'Movie':
                    downloadfromLink(shows_links[id-1], shows[id][1])
                elif shows[id][4] == 'TVShow':
                    pass
                else:
                    downloadfromLink(shows_links[id-1], shows[id][1])
            else:
                print("No show/movie with ID:", id)
        else:
            print("Found 0 shows/movies.")

    except Exception as exception:
        print("Error:", exception.__class__.__name__)
        print("Can't Search. Something goes wrong.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Movie Downloader")
    parser.add_argument("-l", action="store", dest = "link", help="search for video in webpage of given link and downloads it. Other arguments would be ignored.")
    parser.add_argument("-s", action="store", dest = "search", help="search for movie or series with given name which can be downloaded.")

    arguments = parser.parse_args()
    
    if arguments.link != None:
        downloadfromLink(arguments.link)
    if arguments.search:
        searchMovies(arguments.search)
    else:
        print(parser.format_help())
