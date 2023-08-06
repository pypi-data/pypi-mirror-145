from litetable import LiteTable
import pandas as pd


def test_pandas(lt):
    df = pd.DataFrame(lt)
    assert list(df.itertuples(index=False)) == list(lt)


def test_from_pandas(lt):
    df = pd.DataFrame(lt)
    lt2 = LiteTable(df)
    assert list(lt) == list(lt2)

