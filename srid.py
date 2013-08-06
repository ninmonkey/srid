from __future__ import print_function, division
import os
import time
import urllib
import pickle

import praw

SLEEP_IN_SECS = 1.3  # 0.3
version = "0.2.5"
debug = True
ignore_cache = False
stats_downloaded = 0


def load_cache():
    # get last-retrieved
    path = os.path.join("srid-downloaded", "cache.pkl")

    if ignore_cache:
        return (None, None, None)

    try:
        with open(path, "rb") as f:
            cache = pickle.load(f)
            return cache

    except IOError:
        return (None, None, None)


def save_cache(cache):
    # save last-retrieved
    path = os.path.join("srid-downloaded", "cache.pkl")
    with open(path, "wb") as f:
        pickle.dump(cache, f)


def save_url(url, subreddit, title):
    # save for later, like flickr which don't work.
    path = os.path.join("srid-downloaded", "saved_urls.pkl")

    urls = []
    # load prev urls, and append to file
    try:
        with open(path, "rb") as f:
            urls = pickle.load(f)
    except IOError:
        urls = []

    # save if new
    val = (url, subreddit, title)
    if not val in urls:
        urls.append(val)

        with open(path, "wb") as f:
            pickle.dump(urls, f)

        #print("== saved failed urls ==")
        #pprint(urls)
        print("len: ", len(urls))


def sanitize_filename(filename):
    # return a valid filename.
    # win7 says to use these, so it may not be fully correct cross platform,
    # edit `invalid_chars`
    invalid_chars = '\/|*?"<>:'
    only_ascii = filename.encode("ascii", "ignore")
    safe_name = "".join(ch for ch in only_ascii if ch not in invalid_chars)
    return safe_name


def download_file(url, subreddit, title):
    # save from url, to ./srid-downloaded/{subreddit}/{title}
    global stats_downloaded
    ext = os.path.splitext(url)[1].lower()

    # imgur has bad file names
    ext = "".join(ch for ch in ext if ch not in '?1234567890')

    safe_title = sanitize_filename(title)
    folder = os.path.join("srid-downloaded", subreddit)
    filename = os.path.join(folder, safe_title + ext)

    # if url appears to be bad, save for later incase I can preserve it
    #if filename.endswith(".png") or filename.endswith(".jpg"):
    #if ext == "".png") or filename.endswith(".jpg"):
    if any(x == ext for x in ("jpg", "jpeg", "png", "gif")):
        if debug:
            print("good: ", filename)
    else:
        print("bad name?\n\t{}\n\t{}".format(url, filename))
        save_url(url, subreddit, title)

    try:
        os.mkdir(folder)
    except:
        pass

    if debug:
        print("writing...: ", filename)

    # delay if download, count stats
    if not os.path.exists(filename):
        stats_downloaded += 1
        urllib.urlretrieve(url, filename)
        time.sleep(SLEEP_IN_SECS)


def do_filter(likes, subs):
    # filter generator/list that are not in subs
    # Should I instead should delete or use that built in func/class to
    # filter+delete ?

    # load prev cache, save new one
    cache = load_cache()
    cached = False

    print("cache: ", cache)
    print("Downloading: ")

    for cur in likes:
        # save first item downloaded. But I want to keep the generator.
        if not cached:
            save_cache((cur.url, cur.title, cur.subreddit.url))
            cached = True

        # can I quit early?
        if cache == (cur.url, cur.title, cur.subreddit.url):
            print("updated to cached, ending.")
            return

        # if any sub will match.
        if any(sub.lower() in cur.subreddit.url.lower() for sub in subs):
            if debug:
                print("get: ", cur.url, " -- ", cur.subreddit.url)
            download_file(cur.url, cur.subreddit.display_name, cur.title)
            print(".", end="")


def print_debug(likes):
    # view data on submission
    # see also: dir(cur) and pprint(vars(cur))
    for cur in likes:
        print("#")
        print("sub=", cur.subreddit.url)
        print("title=", cur.subreddit.title)
        print("permalink=", cur.permalink)
        print("url=", cur.url)


def main(sub_names, num=10):
    # Very important to get UserAgent part right, including a version number.

    user_agent = ("Srid subreddit image downloader/v{} by u/MonkeyNin "
                "https://github.com/ninmonkey/srid".format(version))
    if debug:
        print("num", num, "\n\tsubs:", sub_names)

    print('user_agent:', user_agent, "\n")
    r = praw.Reddit(user_agent, "nin")  # Set user/pass in praw.ini
    r.login()
    if debug:
        print("logged in? ", isinstance(r.user, praw.objects.LoggedInRedditor))

    # .get_liked() is a generator, will create on-demand
    do_filter(r.user.get_liked(limit=num), sub_names)

if __name__ == "__main__":
    # hardcoded for now, multiple only to simplify groups
    subs_aww = ["aww", "birds", "cats"]
    subs_comics = ["comics"]
    subs_photos = ["NationalGeographic", "EarthPorn", "AnimalPorn", "SpacePorn", "wallpaper", "wallpapers", "itookapicture", "photocritique", "skyporn"]
    subs_imaginary = ["imaginary", "imaginaryArmor", "imaginaryBattlefields", "imaginaryCharacters", "imaginaryCityscapes", "imaginaryLandscapes", "imaginaryRobotics", "imaginaryStarships", "imaginaryTechnology", "imaginaryVehicles", "imaginaryWeaponry", "imaginaryMonsters", "SpecArt", "imaginaryLandscapes", "ImaginaryWildlands"]
    subs_sfw_images = ["lowpoly", "starshipporn", "microporn", "AbandonedPorn", "futurePorn", "AdPorn", "AlbumArtPorn", "ArchitecturePorn", "ArtPorn", "BookPorn", "CityPorn", "DesignPorn", "DestructionPorn", "EarthPorn", "FirePorn", "HistoryPorn", "GeologyPorn", "images", "FossilPorn", "MilitaryPorn", "MapPorn", "MoviePosterPorn", "ColorizedHistory", "BattlePaintings", "FighterJets", "Airplanes", "Helicopters", "WarshipPorn", "Helicopters", "HumanPorn", "OldSchoolCool", "TheWayWeWere", "VintageAds", "PropagandaPosters", "Castles", "concertposterporn", "VHScoverART", "geekporn", "waterporn", "quotesporn", "ruralporn", "macroporn", "winterporn", "ArchitecturePorn", "WQHD_Wallpaper"]
    subs_people = ["ladyladyboners", "Goddesses", "FineLadies", "gentlemanboners", "ClassicScreenBeauties", "ladyladyboners", "ladyboners", "VGB", "VintageLadyBoners", "faces", "classywomenofcolor"]

    subs = subs_aww + subs_comics + subs_photos + subs_imaginary + subs_sfw_images + subs_people

    print("downloading: sleep = {}secs".format(SLEEP_IN_SECS))
    main(subs, num=10)
    print("\nDownloaded new images: {}".format(stats_downloaded))
