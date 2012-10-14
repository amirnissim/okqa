#!/usr/bin/env perl

# $Id$

use 5.10.0;
use common::sense;
use integer;
use English qw(-no_match_vars);
use autodie;

use Getopt::Long qw(:config gnu_getopt);
our %Opts = (port => 1025);
GetOptions(\%Opts, 'port=i');

use AnyEvent::SMTP::Server;

my $server = new AnyEvent::SMTP::Server port => $Opts{'port'};
die unless $server;
say "Listening on port $Opts{'port'}...";
$server->reg_cb(mail => sub {
        my $m = $_[1];
        local $" = ', ';
        my $t = localtime;
        print <<EOF;
============ $t ==============
From: $m->{'from'}
To: @{$m->{'to'}}

$m->{'data'}

EOF
    }
);
$server->start;
AnyEvent->condvar->recv;

