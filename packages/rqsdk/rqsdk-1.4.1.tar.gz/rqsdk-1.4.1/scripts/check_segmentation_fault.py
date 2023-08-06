modules = [
    "numpy",
    "pandas",
    "patsy",
    "statsmodels",
    "scipy",
    "bokeh",
    "rqdatac",
    ("rqfactor", [
        "exception", "interface", "utils", "exception", "_dma", "func", "rolling", "leaf", "fix", "cross_sectional", "engine_v2", "analysis"
    ]),
    "rqoptimizer",
    "rqalpha_plus"
]


def import_module(super_module, module):
    def _complete_module(m):
        if super_module:
            return f"{super_module}.{module}"
        return module

    if isinstance(module, str):
        print(_complete_module(module))
        __import__(_complete_module(module))
    elif isinstance(module, tuple):
        module, sub_modules = module
        for sub_module in sub_modules:
            import_module(_complete_module(module), sub_module)
        import_module(super_module, module)
    else:
        raise NotImplementedError(module)


for m in modules:
    import_module(None, m)