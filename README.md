# Alien Invasion

Alien Invasion is a classic fixed-screen arcade game built with Python and
Pygame. Clear increasingly fast alien fleets, protect your three ships, and
chase a high score that lasts until the application closes.

## Requirements and Setup

Python 3.12 is recommended.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt -r requirements-dev.txt
```

On macOS or Linux, activate with `source .venv/bin/activate` instead.

## Run and Controls

Start the game from the repository root:

```powershell
python alien_invasion.py
```

| Action | Controls |
| --- | --- |
| Move | Left/Right arrows or A/D |
| Fire | Space |
| Start/restart | Enter or click the button |
| Pause/resume | P or Escape |
| Mute/unmute | M |
| Quit | Q or close the window |

## Test

Tests use Pygame's dummy video and audio drivers and do not open a window:

```powershell
python -m pytest -q
python -m compileall alien_invasion.py alien.py bullet.py button.py `
  game_stats.py resources.py scoreboard.py settings.py ship.py sound_manager.py
```

For gameplay changes, also manually check movement boundaries, collisions,
level transitions, life loss, pause, audio, restart, and quitting.

## Build the Windows Executable

```powershell
python -m PyInstaller --clean --noconfirm alien_invasion.spec
.\dist\AlienInvasion.exe --smoke-test
.\dist\AlienInvasion.exe
```

The versioned spec bundles all files under `images/` and `sounds/` into a
windowed, single-file executable. Build artifacts stay in ignored `build/` and
`dist/` directories.

## Troubleshooting

- Run from the repository root when using the Python entry point.
- If audio initialization fails, the game continues silently by design.
- If PowerShell blocks virtual-environment activation, run the environment's
  Python directly: `.\.venv\Scripts\python.exe alien_invasion.py`.
