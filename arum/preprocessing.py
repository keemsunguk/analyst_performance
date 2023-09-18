import pandas as pd
from datetime import datetime
from arum.lookups.recommendations import recommendation_lookup
from arum.lookups.column_names import new_col_names


def fix_price(s_df: pd, col_name: str):
    for i, r in s_df.iterrows():
        if type(r[col_name]) == str:
            s_df.at[i, col_name] = 0
    return s_df


def get_author_production(s_df: pd):
    s_df['author'] = s_df['author'].apply(lambda x: x.strip())
    return dict(s_df['author'].value_counts())


def clean_recommendations(s_df: pd):
    s_df['recommendation'] = s_df['recommendation'].apply(lambda x: recommendation_lookup[x])
    return dict(s_df['recommendation'].value_counts())


def change_col_names(s_df: pd) -> pd:
    return s_df.rename(columns=new_col_names, inplace=True)


def check_report_date(s_df: pd) -> pd:
    for k, r in s_df.iterrows():
        if type(r['report_date']) == str:
            s_df.at[k, 'report_date'] = datetime.strptime(r['report_date'], '%m/%d/%y')
    s_df['report_month'] = s_df['report_date'].apply(lambda x: x.strftime('%Y%m'))
    return s_df


def build_labels(s_df: pd) -> pd:
    """
    A1 = (발간일시가 - 전일종가) / 전일종가
    A2 = (고가 - 시가) / 시가
    A3 = (종가 - 시가) / 시가
    :param s_df:
    :return:
    """
    s_df['__label1'] = s_df.apply(lambda x: 1 if x.A1 > 0 else 0, axis=1)  # 종가 > 어제종가
    s_df['__label2'] = s_df.apply(lambda x: 1 if x.A2 > 0 else 0, axis=1)  # 어제고가 > 종가
    s_df['__label3'] = s_df.apply(lambda x: 1 if x.A3 > 0 else 0, axis=1)  # 어제고가 > 어제종가

    # (시가-전일종가)/전일종가
    s_df['gap_up_ratio'] = s_df.apply(
        lambda x: (x.opening - x.closing_1) / x.closing_1 if x.closing_1 > 0 else -1, axis=1)
    # (당일고가 – 발간일시가)/발간일시가
    s_df['high_profit_ratio'] = s_df.apply(
        lambda x: (x.high - x.opening) / x.opening if x.opening > 0 else -1, axis=1)
    # (당일종가 – 발간일시가)/발간일시가
    s_df['closing_profit_ratio'] = s_df.apply(
        lambda x: (x.closing - x.opening) / x.opening if x.opening > 0 else -1, axis=1)
    return s_df


def group_by_month(v_df: pd) -> dict:
    """
    Rearrange the validated data by month
    :param v_df: validated, sentiment DF
    :return: dict with key by %Y%d string
    """
    monthly_by_author_dict = {}
    mon_key, _ = zip(*(dict(v_df['report_month'].value_counts()).items()))
    for mon in sorted(mon_key):
        tmp = v_df.loc[v_df.report_month == mon]
        author_freq_dict = dict(tmp['author'].value_counts())
        avg_by_author_by_mon = tmp[['author', 'gap_up_ratio', 'high_profit_ratio', 'closing_profit_ratio']].groupby(
            ['author']).mean().copy()
        avg_by_author_by_mon.reset_index(inplace=True)
        avg_by_author_by_mon['author_frequency'] = avg_by_author_by_mon.apply(lambda x: author_freq_dict[x.author],
                                                                              axis=1)
        monthly_by_author_dict[mon] = avg_by_author_by_mon.sort_values('high_profit_ratio', ascending=False)
        monthly_by_author_dict[mon] = monthly_by_author_dict[mon].reset_index()
        monthly_by_author_dict[mon].drop(['index'], inplace=True, axis=1)
    return monthly_by_author_dict
