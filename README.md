loguetools is a set of commandline tools written in Python 3.7+ for Korg minilogue xd programs and preset packs (Korg's name for patches and patch libraries).

# Installation
Install `loguetools` using pip

```bash
pip install loguetools
```

# Usage

All tools are self-documenting; --help will show simple examples.

`dump`

Display the contents of a program (.mnlgprog or .mnlgxdprog) or preset pack (.mnlgpreset or .mnlgxdlib). -m generates md5 checksums for patches.

`explode`

Extract and save programs in a minilogue xd preset pack to separate .mnlgxdprog files.

`translate`

Translate original (OG) minilogue programs (.mnlgprog) and preset packs (.mnlgpreset) to the minilogue xd (.mnlgxdprog and .mnlgxdlib)

# Limitations

I don't own an original minilogue so I have limited ability to test the translation accuracy. I found [Jeff Kistler's minilogue editor](https://github.com/jeffkistler/minilogue-editor) very helpful for checking some of the parameter translations. The hardware and routing possibilities for the OG and xd differ in significant ways. The translate tool tries to make sensible choices about setting the xd's EG and LFO hardware to match the original patch but the options are limited. Korg's documentation has some errors and omissions and I haven't worked out how to translate everything correctly yet; if you notice a problem, please let me know or create an issue!

* Programs named "Init Program" are deliberately skipped

These are on my radar
* No sequence translation yet
* No prologue patch translation yet
* No translation of the joystick y-parameter yet
* Smarter use of the xd multi-engine to switch between noise and sub oscillator
* Improve unit tests

# Known problems
* BPM tempo is obviously wrong. I'm not sure why.
* I haven't created minilogue patch packs that can be distributed. Thus most unit tests will fail. This may improve in future.

# Development notes
Suggestions and bug reports are welcome. Pull requests will probably be welcome.