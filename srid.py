from __future__ import print_function, division
import praw
from pprint import pprint
#import pyimgur

version = "0.1"
debug_force_cached = False

def with_status(iterable):
    """Wrap an iterable outputting '.' for each item (up to 100 per line)."""
    for i, item in enumerate(iterable):
        sys.stderr.write('.')
        sys.stderr.flush()
        if i % 100 == 99:
            sys.stderr.write('\n')
        yield item

    sys.stderr.write('\n')

def do_filter(likes):
	print("## filtered ##")

def do_stuff(likes):
	# see also: dir(cur)
	for cur in likes:
		print("#")
		print("sub=", cur.subreddit.url)
		print("title=", cur.subreddit.title)
		print("permalink=", cur.permalink)
		print("url=", cur.url)



def main(sub_names):
	# Very important to get UserAgent part right, including a version number.
	user_agent = ("Srid subreddit image downloader/{} by u/MonkeyNin https://github.com/ninmonkey/srid".format(version))

	print('user_agent:', user_agent, "\n")
	r = praw.Reddit(user_agent, "nin")
	r.login()
	print("logged in? ", isinstance(r.user, praw.objects.LoggedInRedditor))

	likes = list(r.user.get_liked(10))
	do_stuff(likes)
	do_filter(likes)




def mainold():

	r = praw.Reddit(user_agent=user_agent)

	print("UserAgent:", user_agent)
	for name in subs_names:
		print("sub:", name)

	# one sub only for now
	subreddit = r.get_subreddit("ImaginaryMonsters")
	#submissions = [ i for i in subreddit.get_hot(10) ]
	for submission in subreddit.get_hot(10):
		print('yeah')
		return

	# debug show json
	pprint(vars(submissions[0]))

	print("\n\n== loop ==")
	for cur in submissions:
		title = cur["title"]
		print("post: {}".format(title))




if __name__ == "__main__":
	print("start")
	main(['AnimalPorn', 'SpacePorn'])