#### usage ####

	1. set username/pass in your praw.ini , to find the location:
		https://praw.readthedocs.org/en/latest/pages/configuration_files.html

	2. Run for default subs, and fetch count: 100

#### requirements ####

	- praw

## FIRST ##
	1. change debug to logging

	1. create /root/sub/ if not existing

	1. default bool filter NSFW images
		save to diff root: /srid-downloaded-NSFW/*

	1. flickr doesn't download properly.
		save flickr url posts to a pickle, to download later when implemented

## later ##

	1. imgur urls not cached since filename has no ext. search without it.

	1. grab extension from MIME.

	1. custom location for /srid-downloaded/

	1. check duplicate images, different subsreddits. ( save source url to quickly compare? )

	1. min-image-size 	1. copy wallpaper sized to another dir
	1. more error handling to continue on individual failed images



	1. command args:
		1. count
		2. input filename

	1. save metadata to post url, (tinyurl in filename?)

	1. test gallery images work:
		http://www.reddit.com/r/MicroPorn/comments/19pr0v/fractal_bacteria_colonies_xpost_from_rbiology/

	1. special cases:
		1. /r/redditgetsdrawn/ special case check comments for upvoted images
		1. and special data /r/dataisbeatiful or /r/visualization

		imgur galleries:
			http://imgur.com/a/QqxU6

		servers (flickr/imgur) HTML output sometimes
			flickr does if lightbox links ( when fin.info().getsubtype() == 'html' )

	1. "discover" mode
		-output list of subs in history, if post link is:image.

	1. still 'bad names"'

		http://farm4.staticflickr.com/3815/9367019751_837a4cba99_k.jpg
		srid-downloaded\photocritique\Long Exposure Fingal Beach - Australia.jpg

		http://features.cgsociety.org/newgallerycrits/g54/287154/287154_1183902527_large.jpg
		srid-downloaded\ImaginaryCharacters\Necromant by Ruslan Svobodin.jpg

#### changelog ####

# v0.2.6
	- [todo] Logging module + view /w tail
	- [todo] discover feature

# v0.2.5
	- uses urlopen so MIME and download can use a single request.
	- special behaviours for specific sites (imgur)
	- detect extension from MIME

# v0.2.3
	- less .delay() if file exists
	- cache will quit early if already done. (if submission == last_newest) then quit

# v0.2.2
	- base release version of the script
	- fully working, saves images to ./srid-downloaded/*
	- filters using preset subs
	- converts to safe filenames, including imgur urls: foo.png?1
	- pep8

# v0.1
	- grab lists of upvoted images
