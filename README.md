# loguetools

**loguetools** manipulates Korg 'logue'-series synthesizer patch libraries (what Korg calls program collections).

It perform a few tasks:
* Translation of patches from the (original) minilogue to the minilogue xd. See the [translation](#translation) section for a description and limitations.  
(For *minilogue xd*)
* Bulk extraction of all patches in collections to separate patch files.  
(For *minilogue*, *minilogue xd* and *prologue*)
* Readable display of patch contents.  
(For *minilogue* and *minilogue xd*)

There are two versions:
1. A gui-based version (Windows and MacOS)
2. A set of commandline tools written in Python (3.7 or later)

# Installing
## GUI
Just download and run the latest version from [Releases](https://github.com/gazzar/loguetools/releases/latest).  
The files are single-click executables; no need to install. There are Windows (.exe) and macOS (.app.zip) versions.

## Commandline tools
These require Python 3.7 or later.
Install with pip

```bash
pip install loguetools
```

# Using

## GUI

See the wiki.

## Commandline tools
pip will install the script entry points. All tools contain documention for parameters, e.g. **translate --help**

**dump** (For *minilogue* and *minilogue xd*)  
Display the contents of a program or preset pack. -m generates md5 checksums for patches.

**explode** (For *minilogue*, *minilogue xd* and *prologue*)  
Bulk extraction of individual patches from libraries.

**translate** (For *minilogue xd*)  
Translate (original) minilogue patches to the minilogue xd.


# Limitations

The hardware and routing possibilities for the OG and xd differ in significant ways. The translate tool tries to make sensible choices about setting the xd's EG and LFO hardware to match the original patch but the options are limited.

I don't own an original minilogue so I have limited ability to test the translation accuracy. I found [Jeff Kistler's minilogue editor](https://github.com/jeffkistler/minilogue-editor) very helpful for checking some of the parameter translations. Korg's documentation has some errors and omissions and I haven't worked out how to translate everything correctly yet; if you notice a problem, let me know or create an issue!

These are on my radar
* No prologue patch translation yet
* Smarter use of the xd multi-engine to switch between noise and sub oscillator

# Known problems
* I haven't created minilogue patch packs that can be distributed. Thus most unit tests will fail. This may improve in future.

# Licenses
See LICENSE.txt  
Code released under the 3-clause BSD license.  
Application icon "tools by i cons from the Noun Project"

# Development notes
Suggestions and bug reports are welcome. Pull requests will probably be welcome; feel free to create a feature suggestion first to discuss.
