from __future__ import print_function, division
import praw

version = "0.1"
debug_force_cached = False

def main(subs_names):
	# Very important to get UserAgent part right, including a version number.
	user_agent = ("srid subreddit image downloader/{} by user/MonkeyNin/"
		"MonkeyNin https://github.com/ninmonkey/srid".format(version))

	print("UserAgent:", user_agent)
	for name in subs_names:
		print("sub:", name)

if __name__ == "__main__":
	main(['AnimalPorn', 'SpacePorn'])