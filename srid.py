from __future__ import print_function, division
#from pprint import pprint
#import pickle
import os
import time
import urllib

import praw
#import pyimgur

SLEEP_IN_SECS = 2.  # 0.3
version = "0.2.1"
#debug_force_cached = False
debug = False

stats_downloaded = 0

#def with_status(iterable):
    #"""Wrap an iterable outputting '.' for each item (up to 100 per line)."""
    #for i, item in enumerate(iterable):
        #sys.stderr.write('.')
        #sys.stderr.flush()
        #if i % 100 == 99:
            #sys.stderr.write('\n')
        #yield item

    #sys.stderr.write('\n')


def sanitize_filename(filename):
	# strip invalid chars from filename.
	# win7 says to use these, so it may not be fully correct cross platform
	invalid_chars = '\/|*?"<>:'
	only_ascii = filename.encode("ascii", "ignore")
	safe_name = "".join(ch for ch in only_ascii if ch not in invalid_chars )
	return safe_name

def download_file(url, subreddit, title):
	global stats_downloaded
	# save from url, to ./srid-downloaded/{subreddit}/{title}
	ext = os.path.splitext(url)[1]

	# imgur has bad file names
	ext = "".join(ch for ch in ext if ch not in '?1234567890')

	safe_title = sanitize_filename(title)
	folder = os.path.join("srid-downloaded", subreddit)
	filename = os.path.join(folder, safe_title + ext)

	try:
		os.mkdir(folder)
	except:
		pass

	if debug: print("writing...: ", filename)
	urllib.urlretrieve(url, filename)

	stats_downloaded += 1

def do_filter(likes, subs):
	# instead should delete or use that built in func/class to filter+delete
	# then do work in main()
	for cur in likes:
		if any(sub.lower() in cur.subreddit.url.lower() for sub in subs):
		#if subs[0].lower() in cur.subreddit.url.lower():
			if debug: print("get: ", cur.url, " -- ", cur.subreddit.url)
			download_file(cur.url, cur.subreddit.display_name, cur.title)
			print(".", end="")
			time.sleep(SLEEP_IN_SECS)
		else:
			print("failed: ", cur.subreddit.url)

		# slight delay

def print_debug(likes):
	# see also: dir(cur) and pprint(vars(cur))
	for cur in likes:
		print("#")
		print("sub=", cur.subreddit.url)
		print("title=", cur.subreddit.title)
		print("permalink=", cur.permalink)
		print("url=", cur.url)

def main(sub_names, num=10):
	# Very important to get UserAgent part right, including a version number.

	user_agent = ("Srid subreddit image downloader/v{} by u/MonkeyNin https://github.com/ninmonkey/srid".format(version))
	if debug: print("\tsubs:", sub_names)

	print('user_agent:', user_agent, "\n")
	r = praw.Reddit(user_agent, "nin") # Set user/pass in praw.ini
	r.login()
	if debug: print("logged in? ", isinstance(r.user, praw.objects.LoggedInRedditor))

	# list form
	#likes = list(r.user.get_liked(num))
	#if debug: print_debug(likes)
	#do_filter(likes, sub_names)

	# gen form
	do_filter(r.user.get_liked(limit=num), sub_names)

if __name__ == "__main__":

	subs_photos = ["EarthPorn", "AnimalPorn", "SpacePorn", "wallpaper", "itookapicture", "photocritique"]
	subs_imaginary = ["imaginaryArmor", "imaginaryBattlefields", "imaginaryCharacters", "imaginaryCityscapes", "imaginaryLandscapes", "imaginaryRobotics", "imaginaryStarships", "imaginaryTechnology", "imaginaryVehicles", "imaginaryWeaponry", "imaginaryMonsters", "SpecArt"]
	subs_sfw_images = [ "microporn","AbandonedPorn", "futurePorn", "AdPorn", "AlbumArtPorn", "ArchitecturePorn", "ArtPorn", "BookPorn", "CityPorn", "DesignPorn", "DestructionPorn", "EarthPorn", "FirePorn", "HistoryPorn", "GeologyPorn", "images", "FossilPorn", "MilitaryPorn", "MapPorn", "MoviePosterPorn", "ColorizedHistory", "BattlePaintings", "FighterJets", "Airplanes", "Helicopters", "WarshipPorn", "Helicopters", "HumanPorn", "OldSchoolCool", "TheWayWeWere", "VintageAds", "PropagandaPosters", "Castles", "concertposterporn", "VHScoverART", "geekporn", "waterporn", "quotesporn", "ruralporn", "macroporn", "winterporn"]
	subs_people = [ "PrettyGirls", "Goddesses", "FineLadies", "gentlemanboners", "ClassicScreenBeauties", "ladyladyboners", "ladyboners", "VGB", "VintageLadyBoners", "faces", "classywomenofcolor"]

	subs = subs_photos + subs_imaginary + subs_sfw_images + subs_people
	print("downloading:")
	main(subs, num=100)
	print("\nDownloaded: ", stats_downloaded)