# Echo

This is a script I wrote to practice singing --- you sing into the mic and then it detects when you've stopped singing, and immediately plays it back to you!

Most of the credit goes to this stack overflow answer I used here: https://stackoverflow.com/questions/892199/detect-record-audio-in-python

No AI was used for this script or README. Sharing this script because someone asked for it!

You will need a terminal to run this script! You will also need python installed.

Instructions on running it:

1) set up a venv and install requirement.txt
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) install port-audio
Unfortunately, this depends on which OS you are in.

I did find instructions here: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/scripts/readme-gen/templates/install_portaudio.tmpl.rst

I did this a little while ago on my macbook using brew, but I'd rather link to instructions instead of writing up instructions for something I haven't done recently.

3) Run the script!

One last note --- if you aren't on macos, you might have to substitute the boop sound with another file, or you can comment that section out.
```
python3 main.py
```

Enjoy!

Though this took me an hour to set up, I've been using it for the last few years to practice singing, and it's been pretty useful! I really enjoy little projects like these-- little effort with a lot of payoff!
