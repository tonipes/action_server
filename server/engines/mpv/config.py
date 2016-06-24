from server.engine import EngineProp, EngineAction

props = {
    'pos_time':        EngineProp(["get_property", "time-pos"]),
    'duration':        EngineProp(["get_property", "duration"]),
    'remaining':       EngineProp(["get_property", "time-remaining"]),
    'pos_percent':     EngineProp(["get_property", "percent-pos"]),
    'volume':          EngineProp(["get_property", "volume"]),
    'title':           EngineProp(["get_property", "media-title"]),
    'pause':           EngineProp(["get_property", "pause"]),
    'progress_text':   EngineProp(deps=['pos_time', 'duration'],
        fn=lambda p, d: sec_to_string(p) + ' / ' + sec_to_string(d)),
    'progress_percent':EngineProp(deps=['pos_percent'],
        fn=lambda p: p / 100.0),
    'volume_percent':  EngineProp(deps=['volume'],
        fn=lambda p: p / 100.0),
    'icon_play_pause': EngineProp(deps=['pause'],
        fn=lambda p: 'pause' if not p else 'play-arrow'),
}
actions = {
    'pause':         EngineAction(["cycle", "pause"]),
    'mute':          EngineAction(["cycle", "mute"]),
    'fullscreen':    EngineAction(["cycle", "fullscreen"]),
    'next':          EngineAction(["playlist_next"]),
    'prev':          EngineAction(["playlist_prev"]),
    'seek_fwd':      EngineAction(["seek", 30, "relative"]),
    'seek_back':     EngineAction(["seek", -15, "relative"]),
    'fun':           EngineAction(["show-text", "This is Fun!"]),
    'show_progress': EngineAction(["show-progress"]),
    'mute':          EngineAction(["cycle", "mute"]),
    'volume_up':     EngineAction(deps=['volume'],
        fn=lambda v: ["set_property", 'volume', v + 10]),
    'volume_down':   EngineAction(deps=['volume'],
        fn=lambda v: ["set_property", 'volume', v - 10]),
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
