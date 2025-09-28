default:
	@just --list --unsorted

run:
	python server.py

test:
	bash ./test.sh

setup:
	python -m venv .env
	source .env/bin/activate && pip install -r requirements.txt

# Make a fossil snapshot of the current state
fossil-snapshot:
	fossil add *.py *.md justfile *.sh
	fossil commit -m "updated"



# On MacOS you need to install portaudio, portmidi and libsndfile first
install-pyo-macos:
	brew install portaudio portmidi libsndfile
	export CPATH="$(brew --prefix portmidi)/include:$CPATH"
	export LDFLAGS="-L$(brew --prefix portmidi)/lib $LDFLAGS"
	export CPATH="$(brew --prefix portaudio)/include:$(brew --prefix libsndfile)/include:$CPATH"
	export LDFLAGS="-L$(brew --prefix portaudio)/lib -L$(brew --prefix libsndfile)/lib $LDFLAGS"
	export CPATH="$(brew --prefix libsndfile)/include:$CPATH"
	export LDFLAGS="-L$(brew --prefix libsndfile)/lib $LDFLAGS"
	pip install pyo