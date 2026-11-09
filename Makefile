VERSION := $(shell python3 -c 'import json; print(json.load(open("app.json"))["version"])')

.PHONY: zip clean

# The release zip, as CI builds it, from files.txt.
zip:
	mkdir -p build
	rm -f build/picodeck-burnin-fixer-*.zip
	zip -9 build/picodeck-burnin-fixer-v$(VERSION).zip $$(cat files.txt)

clean:
	rm -rf build
