FILENAMES := $(shell cat anaconda_tarballs.txt)
DATADIR=data
TARBALLDIR=tarballs
TARBALLS := $(addprefix tarballs/, $(FILENAMES))
JSONS :=    $(patsubst %.tar.bz2,data/%.json, $(FILENAMES))
UNMETS :=   $(patsubst %.tar.bz2,data/%.unmet,$(FILENAMES))

# Run scripts/extract-deps.py on each of the tarballs
data/%.json: tarballs/%.tar.bz2
	python scripts/extract-deps.py $< $@

# Merge all of the data from extract-deps into a single file. This file
# gives all the .so files required by and privided by each conda package
dependsdata.json: $(JSONS)
	python scripts/merge-jsons.py 'data/*.json' dependsdata.json

data/%.unmet: tarballs/%.tar.bz2 dependsdata.json
	python scripts/solve-unmet-depends.py --dependsdata dependsdata.json $< $@

unmet-depends.json: $(UNMETS)
	python scripts/merge-jsons.py 'data/*.unmet' unmet-depends.json

anaconda-depends.json: scripts/build-report.py unmet-depends.json
	python scripts/build-report.py unmet-depends.json > anaconda-depends.json

clean:
	rm -rf anaconda-depends.json data

all: anaconda-depends.json
