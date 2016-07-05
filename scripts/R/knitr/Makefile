
%.tex: %.Rnw
	R CMD Sweave $<

%.pdf: %.tex
	pdflatex $<

analysis.pdf: analysis.tex

.PHONY: clean deepclean

clean:
	rm -f *.log *.aux *.tex *.out *.sty


deepclean: clean
	cd cache; rm -f *
