-- taskboard :: frameless desktop-widget WezTerm config
--
-- WHY WezTerm: Windows Terminal and PowerShell's console host CANNOT go
-- borderless — they always draw a title bar / window chrome. WezTerm (and
-- Alacritty) can remove it. Install WezTerm: https://wezterm.org
--
-- HOW TO USE (pick one):
--   1) Copy this file to your home dir as  ~/.wezterm.lua  (i.e.
--      C:\Users\<you>\.wezterm.lua) — WezTerm loads it automatically; OR
--   2) Point WezTerm at it explicitly:
--        wezterm --config-file "C:\Users\<you>\...\taskboard\wezterm.lua"
--
-- Then pin the window ALWAYS-ON-TOP with PowerToys -> Always On Top
-- (default shortcut  Win+Ctrl+T ). The frame is gone; Textual paints the rest.

local wezterm = require 'wezterm'
local config = wezterm.config_builder()

-- frameless: no title bar, no resize border
config.window_decorations = 'NONE'

-- no tab strip (it's a single-purpose widget)
config.enable_tab_bar = false
config.hide_tab_bar_if_only_one_tab = true

-- let the desktop show through a little
config.window_background_opacity = 0.9

-- a snug initial size that fits the widget comfortably
config.initial_cols = 96
config.initial_rows = 30
config.window_padding = { left = 6, right = 6, top = 4, bottom = 4 }

-- dark ground to match the app's palette (#0d1117)
config.color_scheme = nil
config.colors = { background = '#0d1117', foreground = '#e6edf3' }

-- WezTerm opens your normal shell — so you can run taskboard OR any other
-- widget/command in this window. Just type `taskboard` to launch the board.
-- Prefer a DEDICATED window that boots straight into the board? Uncomment:
--   config.default_prog = { 'taskboard' }        -- (or { 'python', '-m', 'taskboard' })

-- ----------------------------------------------------------------------------
-- "toggle the window border" — the app (Textual) CANNOT touch OS window chrome,
-- but WezTerm can at runtime. These are WezTerm key bindings, not app buttons.
-- ----------------------------------------------------------------------------
config.keys = {
  -- Ctrl+Shift+B : flip the frame on/off (NONE <-> TITLE|RESIZE)
  {
    key = 'b',
    mods = 'CTRL|SHIFT',
    action = wezterm.action_callback(function(window, _pane)
      local overrides = window:get_config_overrides() or {}
      if overrides.window_decorations == 'TITLE | RESIZE' then
        overrides.window_decorations = 'NONE'          -- back to frameless
      else
        overrides.window_decorations = 'TITLE | RESIZE' -- show the frame
      end
      window:set_config_overrides(overrides)
    end),
  },
  -- F11 : borderless fullscreen (another way to go frameless)
  { key = 'F11', action = wezterm.action.ToggleFullScreen },
}

return config
