# Zim_plugins
Plugins for Zim wiki

Plugins for https://github.com/jaap-karssenberg/zim-wiki/wiki

* blockdiagrameditor.py - insert a block diagram (see http://blockdiag.com/en/blockdiag/examples.html)
* networkdiagrameditor.py - insert a network diagram (see http://blockdiag.com/en/nwdiag/nwdiag-examples.html)

If `/usr/share/fonts/truetype/msttcorefonts/arial.ttf` font is not installed, change from

```
diagcmd = ('nwdiag', '-a', '--font=/usr/share/fonts/truetype/msttcorefonts/arial.ttf', '-o')
```

to

```
diagcmd = ('nwdiag', '-a', '-o')
```
