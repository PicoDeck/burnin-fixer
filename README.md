# Burn-In Fixer

Exercises the PicoCalc's LCD for [PicoDeck](https://picodeck.net): it cycles
through solid colours, gradients, scan lines, stripes, flashes and random
noise, to help loosen stuck or burned-in pixels. Run it for several minutes.

## Controls

| Key | Gamepad button | Action |
|---|---|---|
| Enter or F4 | A | Next pattern now (each also moves on by itself) |
| Esc or F5 | B | Quit |

It reads `picocalc.gamepad`, so a Bluetooth controller and the bindings in
Settings → Controls work in it; the status bar names A's key. F4 and F5 are A
and B's default keys.

## Install

From the **App Store** on the device (firmware 0.7.0 or later), or copy the
files listed in `files.txt` to `/apps/burnin_fixer/` on the SD card. Its
`app.json` sets `"dirname": "burnin_fixer"`, so the store installs it to the
same folder. Both routes need PicoDeck firmware 0.7.0 or later: the app
calls `picocalc.gamepad.getNavPressed()`, which older firmware lacks.

## Development

`make e2e` runs the tests in PicoDeck's simulator. It needs a PicoDeck
checkout of PicoDeck 0.7.0 or later (its `develop` branch until 0.7.0
ships) with the simulator built (`make simulator` there), at
`~/Projects/PicoDeck/picodeck` or `$PICODECK_ROOT`.

`make zip` builds the release zip from `files.txt`, as CI does. A tag
`v<version>` matching `app.json`'s version publishes it as a release, which
the PicoDeck store lists.

The app was part of the [PicoDeck repository](https://github.com/PicoDeck/picodeck)
(as `apps/burnin_fixer`) until version 1.0.0; its history came with it.
