# Burn-In Fixer

Exercises the PicoCalc's LCD for [PicoDeck](https://picodeck.net): it cycles
through solid colours, gradients, scan lines, stripes, flashes and random
noise, to help loosen stuck or burned-in pixels. Run it for several minutes.

## Keys

| Key | Action |
|---|---|
| Enter | Next pattern now (each also moves on by itself) |
| Esc | Quit |

## Install

From the **App Store** on the device (firmware 0.7.0 or later), or copy the
files listed in `files.txt` to `/apps/burnin_fixer/` on the SD card. Its
`app.json` sets `"dirname": "burnin_fixer"`, so the store installs it to the
same folder.

## Development

`make zip` builds the release zip from `files.txt`, as CI does. A tag
`v<version>` matching `app.json`'s version publishes it as a release, which
the PicoDeck store lists.

The app was part of the [PicoDeck repository](https://github.com/PicoDeck/picodeck)
(as `apps/burnin_fixer`) until version 1.0.0; its history came with it.
