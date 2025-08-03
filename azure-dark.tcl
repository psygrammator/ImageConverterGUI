package require Tk 8.6
package provide ttk::theme::azure-dark 0.1

namespace eval ::ttk::theme::azure-dark {
    variable colors
    array set colors {
        -background #1E1E1E
        -foreground #FFFFFF
        -selectBackground #d17c00
        -selectForeground #ffffff
        -buttonBackground #2D2D30
    }

    ttk::style theme create azure-dark -parent clam -settings {
        ttk::style configure TLabel -background $colors(-background) -foreground $colors(-foreground)
        ttk::style configure TFrame -background $colors(-background)
        ttk::style configure TButton -padding 6 -background $colors(-buttonBackground) -foreground $colors(-foreground)
        ttk::style map TButton -background [list active $colors(-selectBackground)] -foreground [list active $colors(-selectForeground)]
        ttk::style configure TCombobox -padding 4 -background $colors(-background) -foreground $colors(-foreground)
    }
}
