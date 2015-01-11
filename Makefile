lib: lib/bin/activate
lib/bin/activate: requirements.txt
	test -d lib || virtualenv lib
	. lib/bin/activate; pip install --allow-external mysql-connector-python mysql-connector-python;pip install -r requirements.txt;
	touch lib/bin/activate
clean:
	rm -rf lib
