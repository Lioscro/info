.PHONY : install assets resume
DATE=$(shell date +%Y_%m_%d)
LATEX=lualatex
LATEX_FLAGS=-interaction=nonstopmode --output-directory=render --jobname=$(DATE)

# Define path to files.
INFO_NOTEBOOK=Information.ipynb

default:
	make assets
	make resume

install:
	# IMPORTANT: make sure you have LuaLatex installed!
	tlmgr option repository ctan
	tlmgr update --self
	tlmgr install textpos
	tlmgr install isodate
	tlmgr install substr
	tlmgr install titlesec
	tlmgr install fontawesome

assets:
	jupyter nbconvert --to notebook --inplace --execute $(INFO_NOTEBOOK)

resume: resume/resume.tex resume/resume.cls resume/publications.bib
	cd resume && $(LATEX) $(LATEX_FLAGS) resume.tex && cd ..
	cp resume/render/$(DATE).pdf resume/render/latest/latest.pdf
