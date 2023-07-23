# loguetools

**loguetools** manipulates Korg 'logue'-series synthesizer patch libraries (what Korg calls program collections).

It perform a few tasks:
* Translation of patches from the (original) minilogue to the minilogue xd. See the [translation](#translation) section for a description and limitations.  
(For *minilogue xd*)
* Bulk extraction of all patches in collections to separate patch files.  
(For *minilogue*, *minilogue xd*, *prologue*, *monologue*, and *KingKORG*)
* Readable display of patch contents.  
(For *minilogue* and *minilogue xd*)

There are two versions:
1. A gui-based version (Windows and MacOS)
2. A set of commandline tools written in Python (3.7 or later)

# Download
To download the latest version, head to [Releases](https://github.com/gazzar/loguetools/releases/latest)  
For usage instructions, see the [wiki](https://github.com/gazzar/loguetools/wiki)

# Licenses
See LICENSE.txt  
Code released under the 3-clause BSD license.  
Application icon "tools by i cons from the Noun Project"

# Contributors
[Oleg Burdaev](https://github.com/dukesrg/)
* preset bank format
* collapse tool
* monologue and prologue support
  
[Genevieve Buckley](https://github.com/GenevieveBuckley)  
* CI/CD
* Linux build
