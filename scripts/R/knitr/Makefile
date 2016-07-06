
%.tex: %.Rnw
	R CMD Sweave $<

%.pdf: %.tex
	pdflatex $<

mds.updrs.pdf: mds.updrs.tex

.PHONY: clean deepclean

clean:
	rm -f *.log *.aux *.tex *.out *.sty


deepclean: clean
	cd cache; rm -f *
	cd ..
	cd figure; rm -f *
