# Tech: Godot, SteamPipe, Steam Deck

The Godot sections are engine-specific. "Upload with SteamPipe" and "Steam Deck" apply to any engine. For general engine questions, use the project's engine skill if it has one.
Versions here are not fixed: fetch current docs before integrating (https://godotsteam.com, https://partner.steamgames.com/doc/sdk/uploading).

## Do I need the Steamworks API at all?

- To sell on Steam: **no**. A normal export can be uploaded and played without the Steam API.
- Needed only for achievements, Steam Cloud through the API, overlay features, stats, Workshop or multiplayer.
- Steam Cloud also works without code: point Auto-Cloud in Steamworks at the save folder. Godot saves to `user://`, on Windows by default `%APPDATA%\Godot\app_userdata\<project>`, or `%APPDATA%\<name>` with `use_custom_user_dir`.
- Recommendation for a first release: ship without the API, add achievements in an update. Less risk in the build review.

## GodotSteam (Godot)

- Options: GDExtension from the Asset Library (easiest, stock Godot stays) or a precompiled editor with the module.
- The GodotSteam version must match the Godot version and the Steamworks SDK. Check the compatibility table on godotsteam.com.
- Local testing: put `steam_appid.txt` with the App ID next to the exe (testing only, don't ship it), and keep the Steam client running.
- The overlay doesn't work in the editor with Forward+, but does in the exported game launched from Steam. Always test achievements and overlay in a real Steam build.
- List GodotSteam and its license in the game's credits.

## Export (Godot)

- Install export templates matching the Godot version. Preset "Windows Desktop", 64-bit.
- Debug off, console off. Set icon and product info (company, name, version) in the preset.
- Embed the PCK or ship it next to the exe, both work on Steam.
- Test on a second PC without Godot, so missing files or paths show up.
- A Linux build is optional. List it on the store page only if it is tested, or the build review fails.

## Upload with SteamPipe (any engine)

- Tool: `steamcmd` from the Steamworks SDK (`tools/ContentBuilder`). With a GUI: SteamPipe GUI in the SDK.
- Two VDF files: `app_build_<appid>.vdf` (app, description, depots) and `depot_build_<depotid>.vdf` (which folder gets uploaded).
- Upload: `steamcmd +login <user> +run_app_build ..\scripts\app_build_<appid>.vdf +quit`
- Then assign the build to a branch under "Builds" in the Steamworks backend. Use a password-protected beta branch for testing, go live on `default` only after the build review.
- Set the launch option in Steamworks (exe path relative to the depot).
- Never put login details in scripts or the repo. The user types them in their own terminal.

## Steam Deck (any engine)

- Valve rates games for the Deck program (Verified, Playable, Unsupported). A game without controller support usually ends up Unsupported. That doesn't hurt PC sales, but it loses Deck buyers.
- Needed for Verified: full controller use including menus, text readable at 1280 × 800, no required keyboard, prompts show controller buttons.
- If the game already uses input actions and shows bound keys dynamically, add gamepad bindings, button icons and keyboard-free menus as a planned task, not on the side.
