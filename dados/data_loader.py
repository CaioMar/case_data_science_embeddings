import pandas as pd


def load_data(N: int):
    df = pd.read_parquet("dataset.parquet")

    sample_chance = df.razaosocial.value_counts(normalize=True)

    chances = (
        df.merge(sample_chance, left_on="razaosocial", right_index=True)
        .rename(columns={"razaosocial_y": "sample_chance"})
        .sort_values("sample_chance", ascending=False)
        .drop(columns=["razaosocial_x"])[
            ["sample_chance", "razaosocial", "nome_fantasia"]
        ]
        .groupby(["razaosocial", "nome_fantasia"])
        .sum()
        .sort_values("sample_chance", ascending=False)
    )

    # sample without replacement based on the sample_chance
    inputs = (
        chances.sample(n=N, replace=False, weights="sample_chance")
        .reset_index()
        .sort_values("sample_chance", ascending=False)
    )

    return inputs, df
