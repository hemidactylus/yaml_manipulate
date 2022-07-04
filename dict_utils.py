def dict_merge(main, default):
    """
    Pure dict deep-merge function. First dict has precedence.
    """
    if isinstance(main, dict):
        if default and not isinstance(default, dict):
            raise ValueError('Skew-level dictionaries cannot be merged.')
        return {
            k: dict_merge(
                main[k],
                default=({} if default is None else default).get(k),
            ) if k in main else default[k]
            for k in ({} if default is None else default.keys()) | main.keys()
        }
    else:
        return main
