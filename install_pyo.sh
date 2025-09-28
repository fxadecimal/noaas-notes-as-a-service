brew install portaudio portmidi libsndfile liblo
export CPATH="$(brew --prefix portmidi)/include:$CPATH"
export LDFLAGS="-L$(brew --prefix portmidi)/lib $LDFLAGS"
export CPATH="$(brew --prefix portaudio)/include:$(brew --prefix libsndfile)/include:$CPATH"
export LDFLAGS="-L$(brew --prefix portaudio)/lib -L$(brew --prefix libsndfile)/lib $LDFLAGS"
export CPATH="$(brew --prefix libsndfile)/include:$CPATH"
export LDFLAGS="-L$(brew --prefix libsndfile)/lib $LDFLAGS"
export CPATH="$(brew --prefix liblo)/include:$CPATH"
export LDFLAGS="-L$(brew --prefix liblo)/lib $LDFLAGS"
pip install pyo