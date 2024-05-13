.PHONY : install assets resume
DATE=$(shell date +%Y_%m_%d)
LATEX=xelatex
LATEX_FLAGS=-interaction=nonstopmode --output-directory=render --jobname=$(DATE)

# Define path to files.
INFO_NOTEBOOK=Information.ipynb

default:
	make assets
	make resume
	make cv

install:
	# IMPORTANT: only for MacOS and lualatex
	tlmgr option repository ctan
	tlmgr update --self
	tlmgr install textpos
	tlmgr install isodate
	tlmgr install substr
	tlmgr install titlesec
	tlmgr install fontawesome
	tlmgr install etoolbox
	tlmgr install xifthen
	tlmgr install ifmtarg
	tlmgr install lualatex-math
	tlmgr install sourcesanspro

assets:
	jupyter nbconvert --to notebook --inplace --execute $(INFO_NOTEBOOK)

resume: resume/resume.tex resume/resume.cls
	cd resume && $(LATEX) $(LATEX_FLAGS) resume.tex && cd ..
	cp resume/render/$(DATE).pdf resume/render/latest/latest.pdf

cv: cv/cv.tex cv/cv.cls cv/categories/*.tex
	cd cv && $(LATEX) $(LATEX_FLAGS) cv.tex && cd ..
	cp cv/render/$(DATE).pdf cv/render/latest/latest.pdf
