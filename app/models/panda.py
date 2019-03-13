# %%
import pandas as pd


OLD_PERCENTAGE = .7
NEW_PERCENTAGE = .88
EPIC_DAY = pd.Timestamp(2018, 7, 1)
TD = pd.Timedelta('45 days')
NONE_SIGN = '✖️'


def df_extract(df, attr):
    tmpls = list()
    for r in df:
        tmpls.append(getattr(r, attr))
    return tmpls


def percent_calc(df1, df2):
    tmpls = list()
    for r in zip(df1, df2):
        day, money = r[0], r[1]
        if day < EPIC_DAY:
            tmpls.append(money * OLD_PERCENTAGE)
        else:
            tmpls.append(money * NEW_PERCENTAGE)
    return tmpls


def percent_view(df):
    tmpls = list()
    for day in df:
        if day < EPIC_DAY:
            tmpls.append('70%')
        else:
            tmpls.append('88%')
    return tmpls


def payout(df):
    summator = int()
    tmpls = list()
    for r in df:
        summator += r
        if summator < 100:
            tmpls.append(NONE_SIGN)
        else:
            tmpls.append(round(summator, 2))
            summator = 0
    return tmpls


def payday(df, df2):
    tmpls = list()
    for r in zip(df, df2):
        payout, day = r[0], r[1]
        if payout == NONE_SIGN:
            tmpls.append(NONE_SIGN)
        else:
            tmpls.append(day.date() + TD)
    return tmpls


def epgvay_calc(df, df1):
    p = df[df1 < EPIC_DAY]['Net Sales'].sum()
    a = p * NEW_PERCENTAGE
    b = p * OLD_PERCENTAGE
    return a - b


def epic_give_away(df, df2, fn):
    tmpls = list()
    is_payed = False

    for r in zip(df, df2):
        pay, percent = r[0], r[1]

        predicate_1 = percent == '88%'
        predicate_2 = is_payed == False
        predicate_3 = pay != NONE_SIGN

        if predicate_1 and predicate_2 and predicate_3:
            tmpls.append(pay + fn)
            is_payed = True

        else:
            tmpls.append(pay)
    return tmpls


def pandas_processing(file):

    df = pd.read_csv(file)
    df = df[:-1].iloc[::-1].reset_index(drop=True)
    df['Day'] = pd.to_datetime(df.Day)
    df['Net Sales'] = df['Net Sales'].str.lstrip('$').astype(float)


    df['Gross Sales'] = percent_calc(df.Day, df['Net Sales'])
    df['Percentage'] = percent_view(df.Day)


    df['Year'] = df_extract(df.Day, 'year')
    df['Month'] = df_extract(df.Day, 'month')


    df['Payout'] = payout(df['Gross Sales'])
    df['Pay Day'] = payday(df.Payout, df.Day)


    df['Payout'] = epic_give_away(
                                    df.Payout,
                                    df.Percentage,
                                    epgvay_calc(
                                        df, df.Day
                                    )
                                )


    grdf = df.groupby(
        [
            'Year',
            'Month',
        ]
    ).agg(
            {
                'Day': 'last',
                'Percentage': 'first',
                'Net Units': sum,
                'Net Sales': sum,
                'Gross Sales': sum,
            }
    )

    grdf['Payout'] = payout(grdf['Gross Sales'])
    grdf['PayDay'] = payday(grdf.Payout, grdf.Day)
    grdf['Payout'] = epic_give_away(
                        grdf.Payout,
                        grdf.Percentage,
                        epgvay_calc(grdf, grdf.Day)
    )

    grdf = grdf.drop(['Day'], axis=1)
    grdf = grdf.round(2)
    return grdf.to_html(classes='pandas', escape=False)
