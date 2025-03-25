from fastapi import FastAPI
import yfinance as yf 

app = FastAPI()

@app.get("/data/ticker/{symbol}")
def get_stock_data(symbol: str, period: str = '1mo', frequency: str = "1d"):
    """
    Get historical markerìt data for a given ticker symbol.
    :param symbol: Stock ticker symbol
    :param period: Data period (e.g., 1d, 1m, 1y)
    :param frequency: Sampling frequency of data (e.g., 1d, 1m, 3m)
    """

    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period, interval=frequency) # return a DataFrame
        indicators = calculate_indicators(data)

        return indicators.to_dict()
    except Exception as e:
        return {'Error': str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)