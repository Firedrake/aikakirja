#!/usr/bin/perl -w
#
#  This is a simple script which is designed to accept comment requests,
# and save the details to local text files upon the localhost.
#
#  This code is very simple and should be easy to extend with anti-spam
# at a later point.
#
#
###
#
#   NOTE:  If you wish to use this you must edit three things at the
#         top of the script.
#
#          1.  The directory to save the comment data to.
#
#          2.  The email address to notify.
#
#          3.  The email address to use as the sender.
#
####
#
# Steve
# --
#



use strict;
use warnings;

use CGI;
use POSIX qw(strftime);
use Text::Markdown qw(markdown);


#
#  The directory to store comments in.
#
# NOTE:  This should be writeable to the www-data user, and shouldn't
#        be inside your web-root - or you open up security hole.
#
my $COMMENT = "CHANGEME_PATH_TO_COMMENTS";
#

#
#  The notification addresses - leave blank to disable
#
my $TO   = 'CHANGEME_ADDRESS_TO_SEND_COMMENTS';
my $FROM = 'CHANGEME_SOURCE_ADDRESS_FOR_COMMENTS';


#
#  Find sendmail
#
my $SENDMAIL = undef;
foreach my $file (qw ! /usr/lib/sendmail /usr/sbin/sendmail !)
{
    $SENDMAIL = $file if ( -x $file );
}


#
#  Get the parameters from the request.
#
my $cgi = new CGI();

my $name = $cgi->param('name')    || undef;
my $mail = $cgi->param('mail')    || undef;
my $body = $cgi->param('body')    || undef;
my $id   = $cgi->param('id')      || undef;
my $cap  = $cgi->param('captcha') || undef;
my $link = $cgi->param('link')    || undef;


#
#  If any are missing just redirect back to the blog homepage.
#
if ( !defined($name) ||
     !length($name) ||
     !defined($mail) ||
     !length($mail) ||
     !defined($body) ||
     !length($body) ||
     !defined($id) ||
     !length($id) )
{
    print "Location: http://" . $ENV{ 'HTTP_HOST' } . "/\n\n";
    exit;
}

#
#  Does the captcha value contain text?  If so spam.
#
if ( defined($cap) && length($cap) )
{
    print "Location: http://" . $ENV{ 'HTTP_HOST' } . "/\n\n";
    exit;
}

$body=markdown($body);

#
#  Otherwise save them away.
#
#
#  ID.
#
#if ( $id =~ /^(.*)[\/\\](.*)$/ )
#{
#    $id = $2;
#}


#
#  Show the header
#
print "Content-type: text/html\n\n";


#
# get the current time
#
my $timestr = strftime "%d-%B-%Y-%H:%M:%S", gmtime;


#
#  Open the file.
#
(my $idd=$id) =~ s/.*\///;
$idd =~ s/[^a-z0-9\/]/_/gi;
my $file = $COMMENT . "/" . $idd . "." . $timestr;

open( FILE, ">", $file );
print FILE "Name: $name\n";
print FILE "Mail: $mail\n";
print FILE "Page: $id\n";
print FILE "Date: ".strftime('%a, %d %b %Y %T %z',localtime)."\n";
print FILE "User-Agent: $ENV{'HTTP_USER_AGENT'}\n";
print FILE "IP-Address: $ENV{'REMOTE_ADDR'}\n";
print FILE "Link: $link\n" if ($link);
print FILE "\n";
print FILE "$body";
close(FILE);


#
#  Send a mail.
#
if ( length($TO) && length($FROM) && defined($SENDMAIL) )
{
    open( SENDMAIL, "|$SENDMAIL -t -f $FROM" );
    print SENDMAIL "To: $TO\n";
    print SENDMAIL "From: $FROM\n";
    print SENDMAIL "Subject: New Comment [$id]\n";
    print SENDMAIL "\n";
    print SENDMAIL "$name <$mail>";
    print SENDMAIL "\n\n";
    print SENDMAIL $body;
    close(SENDMAIL);
}

#
#  Now show the user the thanks message..
#
print <<EOF;
<html>
 <head>
  <title>Thanks For Your Comment</title>
 </head>
 <body>
  <h2>Thanks!</h2>
  <p>Your comment will be included the next time this blog is rebuilt.</p>
  <p><a href="http://$ENV{'HTTP_HOST'}/$id">Return to blog</a>.</p>
 </body>
</html>
EOF
