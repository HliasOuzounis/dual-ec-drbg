# Makefile for LaTeX project using latexmk, lualatex, and -shell-escape
MAINFILE = report

LATEXMK = latexmk
LATEXENGINE = lualatex
FLAGS = -shell-escape -output-directory=./tex-out -silent

all: $(MAINFILE).pdf

$(MAINFILE).pdf: $(MAINFILE).tex references.bib $(shell find sections -type f -name '*.tex') preamble.sty
	$(LATEXMK) -pdf -$(LATEXENGINE) $(FLAGS) $(MAINFILE).tex
	mv tex-out/$(MAINFILE).pdf .

clean:
	$(LATEXMK) -c

view:
	make all
	evince $(MAINFILE).pdf &

help:
	@echo "Available targets:"
	@echo "  all      - Build the PDF"
	@echo "  clean    - Remove temporary files"
	@echo "  help     - Show this help message"
	@echo "  view     - Build and open the PDF in a viewer"

.PHONY: all clean view help
