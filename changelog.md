#### usage ####

	1. set username/pass in your praw.ini , to find the location:
		https://praw.readthedocs.org/en/latest/pages/configuration_files.html

	2. Run for default subs, and fetch count: 100

#### requirements ####

	- praw

## FIRST ##

	1. default bool filter NSFW images
		save to /srid-downloaded-NSFW/*

	1. *save* failed downloaded urls, incase imgur:gallery or flickr posts

	1. log amount of *new* images

	1. create /root/sub/ if not existing

## later ##

	1. if submission == last_newest, then quit early

	1. grab extension from MIME.

	1. custom location for /srid-downloaded/

	1. check duplicate images, different subsreddits. ( save source url to quickly compare? )

	1. min-image-size 	1. copy wallpaper sized to another dir
	1. more error handling to continue on individual failed images

	1. change debug to logging

	1. command args:
		1. count
		2. input filename

	1. save metadata to post url, (tinyurl in filename?)

	1. test gallery images work:
		http://www.reddit.com/r/MicroPorn/comments/19pr0v/fractal_bacteria_colonies_xpost_from_rbiology/

	1. special cases:
		1. /r/redditgetsdrawn/ special case check comments for upvoted images
		1. and special data /r/dataisbeatiful or /r/visualization

#### changelog ####

# v0.2.3
	- less .delay() if file exists
	- cache will quit early if already done

# v0.2.2
	- base release version of the script
	- fully working, saves images to ./srid-downloaded/*
	- filters using preset subs
	- converts to safe filenames, including imgur urls: foo.png?1
	- pep8

# v0.1

	- grab lists of upvoted images
