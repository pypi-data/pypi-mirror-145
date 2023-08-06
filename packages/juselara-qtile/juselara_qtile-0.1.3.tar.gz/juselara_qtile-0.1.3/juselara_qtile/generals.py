from libqtile.config import Group, Screen, Match
from libqtile import layout, bar, widget
from juselara_qtile.dataclasses import Keys, PathsConfig 
from typing import List, Dict

def load_groups(keys: Keys) -> List[Group]:
    items = keys.keygroups.dict().items()
    group_vals = map(lambda x: x[1], items)
    valid_groups = filter(lambda x: x is not None, group_vals)
    group_names = map(lambda x: x[-1], valid_groups)
    return list(map(lambda x: Group(x), group_names))

def load_layouts(config: PathsConfig) -> List:
    return [
            layout.Columns(
                margin=config.spacing.margin,
                border_width=config.spacing.border_width,
                border_focus=config.colors.color0,
                border_normal=config.colors.color1
                )
            ]

def load_float_layouts(config: PathsConfig) -> layout.Floating:
    return layout.Floating(
            float_rules=[
                *layout.Floating.default_float_rules
                ]
            )

def load_widget_defaults(config: PathsConfig) -> Dict:
    return {
            "font": config.font.font,
            "fontsize": config.font.fontsize
            }

def create_screens(config: PathsConfig) -> List:
    screens = []
    for _ in range(config.defaults.n_screens):
        screen = Screen(
                wallpaper=config.defaults.wallpaper,
                wallpaper_mode=config.defaults.wallpaper_mode,
                top=bar.Bar(
                    [
                        widget.GroupBox(
                            background=config.colors.color0,
                            padding_x=config.spacing.padding,
                            padding_y=config.spacing.padding,
                            active=config.colors.color1,
                            inactive=config.colors.color5,
                            block_highlight_text_color=config.colors.color4,
                            highlight_method="block",
                            this_current_screen_border=config.colors.color1,
                            this_screen_border=config.colors.color0,
                            other_screen_border=config.colors.color0,
                            other_current_screen_border=config.colors.color0,
                            rounded=True,
                            disable_drag=True,
                            markup=True,
                            font=config.font.font,
                            fontsize=config.font.fontsize
                            ),
                        widget.Spacer(),
                        widget.Image(
                            filename=config.defaults.ram,
                            margin=config.spacing.margin,
                            ),
                        widget.MemoryGraph(
                            border_color=config.colors.color1,
                            graph_color=config.colors.color1,
                            ),
                        widget.Image(
                            filename=config.defaults.cpu,
                            margin=config.spacing.margin,
                            ),
                        widget.CPUGraph(
                            border_color=config.colors.color1,
                            graph_color=config.colors.color1,
                            ),
                        widget.Sep(
                            linewidth=config.spacing.line_width,
                            padding=config.spacing.padding
                            ),
                        widget.Clock(
                            format=config.defaults.time_format,
                            foreground=config.colors.color1,
                            padding=config.spacing.padding,
                            font=config.font.font,
                            fontsize=config.font.fontsize
                            ),
                        widget.Sep(
                            linewidth=config.spacing.line_width,
                            padding=config.spacing.padding
                            )
                        ],
                    size=config.spacing.bar_size,
                    background=config.colors.color0,
                    margin=config.spacing.margin
                    )
                )
        screens.append(screen)
    return screens
