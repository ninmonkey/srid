from __future__ import print_function, division
import praw
from pprint import pprint
#import pyimgur

version = "0.2"
debug_force_cached = False
debug = False

def with_status(iterable):
    """Wrap an iterable outputting '.' for each item (up to 100 per line)."""
    for i, item in enumerate(iterable):
        sys.stderr.write('.')
        sys.stderr.flush()
        if i % 100 == 99:
            sys.stderr.write('\n')
        yield item

    sys.stderr.write('\n')

def filter_save(url, subs):
	# equiv of: "earth" in u'/r/EarthPorn'
	for s in subs:
		if s.lower() in url.lower(): return True
	return False



def do_filter(likes, subs):
	# instead should delete or use that built in func/class to filter+delete
	# then do work in main()
	print("## filtered ##")
	for cur in likes:
		#print(cur.subreddit.url)
		#if not subs in cur.subreddit.url:
			#continue
		#if filter_save(cur.subreddit.url, subs):
			#print("no", cur.permalink)
		if subs[0].lower() in cur.subreddit.url.lower():
			print("get: ", cur.url, " -- ", cur.subreddit.url)
		else:
			print("failed: ", cur.subreddit.url)


		# download url

		#SEE CHANGELOT FOR TODO


def print_debug(likes):
	# see also: dir(cur)
	for cur in likes:
		print("#")
		print("sub=", cur.subreddit.url)
		print("title=", cur.subreddit.title)
		print("permalink=", cur.permalink)
		print("url=", cur.url)

def main(sub_names, num=10):
	# Very important to get UserAgent part right, including a version number.
	user_agent = ("Srid subreddit image downloader/v{} by u/MonkeyNin https://github.com/ninmonkey/srid".format(version))
	print("\tsubs:", sub_names)

	print('user_agent:', user_agent, "\n")
	r = praw.Reddit(user_agent, "nin") # Set user/pass in praw.ini
	r.login()
	print("logged in? ", isinstance(r.user, praw.objects.LoggedInRedditor))

	likes = list(r.user.get_liked(num))

	if debug: print_debug(likes)
	do_filter(likes, sub_names)

if __name__ == "__main__":

	subs_photos = ["EarthPorn", "AnimalPorn", "SpacePorn", "wallpaper", "itookapicture", "photocritique"]
	subs_imaginary = ["imaginaryArmor", "imaginaryBattlefields", "imaginaryCharacters", "imaginaryCityscapes", "imaginaryLandscapes", "imaginaryRobotics", "imaginaryStarships", "imaginaryTechnology", "imaginaryVehicles", "imaginaryWeaponry", "imaginaryMonsters", "SpecArt"]
	subs_sfw_images = [ "microporn","AbandonedPorn", "futurePorn", "AdPorn", "AlbumArtPorn", "ArchitecturePorn", "ArtPorn", "BookPorn", "CityPorn", "DesignPorn", "DestructionPorn", "EarthPorn", "FirePorn", "HistoryPorn", "GeologyPorn", "images", "FossilPorn", "MilitaryPorn", "MapPorn", "MoviePosterPorn", "ColorizedHistory", "BattlePaintings", "FighterJets", "Airplanes", "Helicopters", "WarshipPorn", "Helicopters", "HumanPorn", "OldSchoolCool", "TheWayWeWere", "VintageAds", "PropagandaPosters", "Castles", "concertposterporn", "VHScoverART", "geekporn", "waterporn", "quotesporn", "ruralporn", "macroporn", "winterporn"]
	subs_people = [ "PrettyGirls", "Goddesses", "FineLadies", "gentlemanboners", "ClassicScreenBeauties", "ladyladyboners", "ladyboners", "VGB", "VintageLadyBoners", "faces", "classywomenofcolor"]

	subs = subs_photos + subs_imaginary + subs_sfw_images + subs_people
	main(subs, num=10)