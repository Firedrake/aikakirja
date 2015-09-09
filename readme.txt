=Introduction

aikakirja is a lightweight blogging engine partly based on Steve
Kemp's Chronicle <http://www.steve.org.uk/Software/chronicle/>.

Note that this is code written for personal use and may contain
unexpected bugs.

=Copyright

Yokosou is Copyright 2015 Roger Bell_West.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

=Use

Before deploying any file, change anything labelled CHANGEME.
Eventually this will all become configuration.

aikakirja itself is a blog compiler, using markdown or org-mode to
convert plain text to blog posts. It needs a configuration file, by
default ./config.yaml; a sample is provided.

comment_days: number of days after posting to allow comments
comments: path to comments that get used
db: path to sqlite database
format: default format for processing new posts
frontpage_posts: number of posts to show on front page
org: path to your org-mode definition. Not needed if you don't use org-mode.
postfile: URL format (with strftime expansion) for individual posts.
source: path to text
rss_posts: number of posts to show in RSS feed
rss_comments: number of comments to show in RSS feed
tagdir: path under target for tag indices and feeds
target: path to HTML output
template: path to templates
title: name of the blog
top_ext: absolute URL to the front page of the blog (e.g. http://my.blog.site/)
top_int: relative URL to the front page of the blog (e.g. /)

Create directories to match "source" and "target", and "comments/all",
"comments/good", "comments/spam" and "comments/unknown". Put blog
posts in "source". They should contain some of:

Date: 26 July 2015 09:03
Title: this is my new blog
Tags: I have a blog, another tag, more tags
Xrefs: textfile_for_another_post.txt

Run aikakirja to rebuild any changed pages. If you want to rebuild
everything, delete the sqlite database first.

comments.cgi, based largely on Steve Kemp's equivalent for chronicle,
stores a comment and mails a copy to the blog owner. Put it where the
web server can see it.

chron is a typical wrapper, for a blog maintained on a desktop machine
and published to a remote server accessible via ssh: it copies new
comments from the remote to the local server, runs sort_comments to
classify them, and potentially rebuilds the blog and syncs it to the
server.

sort_comments does comment classification. Put known bad phrases into
comments/fail.yaml as:

---
- \bseo\b
- targeted traffic

etc. and known good correspondents/IP addresses into
comments/pass.yaml as:


---
Mail:
  - good@address
IP-Address:
  - good.ip

. No comment will go live unless you approve it, either by putting a
key into pass.yaml or by manually moving it from comments/unknown to
comments/good.

publish is a system for publishing new posts, based on when the last
post in a category was made and on how many are waiting to be posted.
Pending posts go in pending/ and should take the form:

maincategory_number_title.txt

as:

book_209_a_place_of_confinement.txt

If a post is named with an initial MMDD, as:

1006_book_209_a_place_of_confinement.txt

then (a) it will be posted on that day and (b) nothing else in that
maincategory will be posted until it has been.

Run publish without arguments to see what will be posted next, or with
-d to move the post into entries/ and run chron.

The templates are basically Steve's, only lightly modified.

=Warning

Note that this is not the full code. In my own installation I have a
section in aikakirja to generate a list of all reviewed books, and in
publish to post selected blog entries to selected newsgroups. If there
is a demand for these I will set them as configuration entities and
add them into the public code.
