# Simple actions.
config = {
    'actions': {
        'action_pause':         ["cycle", "pause"],
        'action_mute':          ["cycle", "mute"],
        'action_fullscreen':    ["cycle", "fullscreen"],
        'action_next':          ["playlist_next"],
        'action_prev':          ["playlist_prev"],
        'action_seek_fwd':      ["seek", 30, "relative"],
        'action_seek_back':     ["seek", -15, "relative"],
        'action_fun':           ["show-text", "This is Fun!"],
        'action_show_progress': ["show-progress"],
        'action_mute':          ["cycle", "mute"],
    },

    # Simple properties.
    'properties': {
        'prop_pos_time':     ["get_property", "time-pos"],
        'prop_duration':     ["get_property", "duration"],
        'prop_remaining':    ["get_property", "time-remaining"],
        'prop_pos_percent':  ["get_property", "percent-pos"],
        'prop_volume':       ["get_property", "volume"],
        'prop_title':        ["get_property", "media-title"],
        'prop_pause':        ["get_property", "pause"],
    },

    # Properties that need some custom calculation.
    'calculated_props': {
        'calc_progress_text': (['prop_pos_time', 'prop_duration'],
            lambda p, d: sec_to_string(p) + ' / ' + sec_to_string(d)
        ),
        'calc_progress_percent': (['prop_pos_percent'],
            # Client needs progress between 0.0 and 1.0
            lambda p: p / 100.0
        ),
        'calc_volume_percent': (['prop_volume'],
            # Client needs progress between 0.0 and 1.0
            lambda p: p / 100.0
        ),
        'calc_icon_play_pause': (['prop_pause'],
            lambda p: 'pause' if not p else 'play-arrow'
        )
    },

    # Actions that need some custom calculation.
    'calculated_actions': {
        'calc_actions_volume_up': (['prop_volume'],
            lambda v: ["set_property", 'volume', v + 10]
        ),
        'calc_actions_volume_down': (['prop_volume'],
            lambda v: ["set_property", 'volume', v - 10]
        )
    },
}
###########
# Helpers #
###########

def sec_to_string(sec):
    sec = round(sec)
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    res = "{:0>2d}".format(h) + ':' if h > 0 else ''
    res += "{:0>2d}".format(m) + ':' + "{:0>2d}".format(s)
    return res
