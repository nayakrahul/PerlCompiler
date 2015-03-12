switch ($val) {
		case 1		{ print "number 1";}
		case "a"	{ print "string a";}
		case 2	{ print "number in list"; }
		case 3	{ print "number in list"; }
		case 4	{ print "pattern"; }
		case (3+4)*3	{ print "pattern"; }
		case "hello"	{ print "entry in hash"; }
		case 7.98	{ print "entry in hash"; }
		case 0b0010	{ print "arg to subroutine"; }
		else		{ print "previous case not true"; }
	}