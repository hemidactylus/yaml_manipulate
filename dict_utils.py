def dict_merge(main, default, c_path=[]):
    """
    Pure dict deep-merge function. First dict has precedence.
    """
    if isinstance(main, dict):
        if default and not isinstance(default, dict):
            print(str(c_path))
            raise ValueError('Skew-level dictionaries cannot be merged at %s' % ('.'.join(c_path)))
        return {
            k: dict_merge(
                main[k],
                default=({} if default is None else default).get(k),
                c_path=c_path + [(k if isinstance(k, str) else '[%i]' % k)]
            ) if k in main else default[k]
            for k in ({} if default is None else default.keys()) | main.keys()
        }
    else:
        return main
