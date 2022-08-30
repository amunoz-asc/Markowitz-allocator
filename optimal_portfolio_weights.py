def optimal_portfolio_weights(stocks, weights):
    if stocks.size == 0:
        df = pd.DataFrame({"Weights": weights})
    else:
        df = pd.DataFrame({"Stock": stocks,
                       "Weights": weights})
        df=df.set_index('Stock')
    df.Weights = df.Weights.map(lambda x: '{:.5%}'.format(x))
    return df
