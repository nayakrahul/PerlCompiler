all: src/plexer.py src/parser.py
	cp src/plexer.py bin/plexer.py
	cp src/parser.py bin/parser.py
	cp src/parsetree.py bin/parsetree.py
	chmod +x bin/plexer.py
	chmod +x bin/parser.py
	chmod +x bin/parsetree.py
clean:
	rm -f bin/*