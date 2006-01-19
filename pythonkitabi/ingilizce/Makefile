# Makes HTML via jade and Docbook.
export SGML_CATALOG_FILES=/usr/local/cmd/dtd/sgml/docbook.cat:/usr/local/cmd/dbsgml/catalog

all: book.sgml
	-/usr/local/cmd/bin/openjade -V html-index -t sgml -d /usr/local/cmd/dbsgml/html/docbook.dsl book.sgml

index: book.sgml
	-perl /usr/local/cmd/dbsgml/bin/collateindex.pl -N -o index.sgml
	/usr/local/cmd/bin/openjade -V html-index -t sgml -d /usr/local/cmd/dbsgml/html/docbook.dsl book.sgml
	perl /usr/local/cmd/dbsgml/bin/collateindex.pl -g -o index.sgml HTML.index

bookps: book.sgml
	-dbsgml ps book.sgml

pdf: book.sgml
	-db2ps book.sgml
	dvips -f book.dvi -o book.ps
	ps2pdf book.ps book.pdf

clean: 
	-rm *htm -f