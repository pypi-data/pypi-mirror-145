import pandas as pd


def get_color_scheme(scheme_name):

    scheme = pd.read_table(
        'https://raw.githubusercontent.com/vega/vega/v5.21.0/packages/vega-scale/src/palettes.js',
        skipinitialspace=True,
        sep=':',
    ).loc[
        scheme_name
    ].str.replace(
        "'",
        ""
    ).apply(
        lambda x: ["#" + x[i:i+6] for i in range(0, len(x), 6)]
    )[0]

    return scheme[0:-1]
