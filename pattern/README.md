# SteamShip pattern mirror (`haker146/SteamShip`, branch `pattern`)

Same layout as [KoriaPolis/Steam-Auto-PT](https://github.com/KoriaPolis/Steam-Auto-PT/tree/pattern).

LumaCore.dll at Steam start:

1. Local cache
   - `<Steam>/lumacore/pattern/<sha256>.toml` (steamclient / steamui)
   - `<Steam>/lumacore/pattern/steamclientipc/<sha256>.toml` (IPC)
2. This repo, branch `pattern`: `{subdir}/{sha}.toml`
3. Fallback: `KoriaPolis/Steam-Auto-PT` branch `pattern`

```
steamclient/<sha256>.toml
steamui/<sha256>.toml
steamclientipc/<sha256>.toml
```

`lumacore.toml` written by SteamShip Auto LC Setup:

```toml
[pattern_fetch]
mirror = "https://raw.githubusercontent.com/haker146/SteamShip/pattern/{subdir}/{sha}.toml"
```

DLL releases stay on `KoriaPolis/LumaCore`. This tree currently includes Steam client build **1788400362**.
