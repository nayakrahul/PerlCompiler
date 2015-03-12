use strict;
use warnings;

for ( $x=1;$x<9;$x++) 
	{ 
		$total = $x;                
	}
	print "The total from 1 to 100"; 
	print 'The total from 1 to 100';


	print "Which Metric jaccard or Bleu:";
my $metric=<>;
	print "Which source title or snippet or url:";
my $source=<>;
if($metric eq "jaccard")
	{
		if($source eq "title")
		{
			if(1)
				print "in title";
		}
		elsif($source eq "snippet")
		{
			print "in snippet";
		}
		elsif($source eq "url")
		{
			print "in url";
			print"jaccard method not called";
		}
		else
		{
			print "jacccard not called";
		}
	}
elsif($metric eq "bleu")
	{
		print "bleu called";
	}
else
	{
	print "bleu not called";
	}