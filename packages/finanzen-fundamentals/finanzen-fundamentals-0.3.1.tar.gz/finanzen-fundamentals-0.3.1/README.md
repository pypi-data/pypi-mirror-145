# Finanzen-Fundamentals
Finanzen-Fundamentals is a library designed to parse fundamentals and prices for multiple instruments (currently supported instruments are: stocks, funds, ETFs, and commodities) from [Finanzen.net](https://www.finanzen.net/). Finanzen.net is a large German financial news website which also offers free access to a huge database containing financial information. This library is designed to query information on Finanzen.net from within Python. In order to make the library accessible to non-German speakers, it was designed with English as the primary language. Note however, there is no translation of German information that comes from Finanzen.net such as actual values.

# Installation
You can easily install Finanzen-Fundamentals via pip by running `pip install finanzen-fundamentals`.

# Usage
## Importing
Every instrument has its own module within Finanzen-Fundamentals. You can import these modules like so:

```
import finanzen_fundamentals.stocks as stocks
import finanzen_fundamentals.funds as funds
import finanzen_fundamentals.etfs as etfs
import finanzen_fundamentals.commodities as commodities
```

## Searching
For all functions in Finanzen-Fundamentals, you need to provide the name of the instrument. For this you will have to provide the special Finanzen.net name. To find out the correct name, you can use the search functionality in all modules. This function takes a search query and the maximum number of results you would like to get. Note that you will get at maximum 30 entries.

```
stocks.search_stock("BMW", limit=3)
funds.search_fund("Private Equity", limit=10)
etfs.search_etf("iShares", limit=10)
commodities.search_commodity("Kohle", limit=3)
```

The *search_stock* function will return a list of dictionaries. Each dictionary might contain the following keys: "Name" (official name), "Stock" (name used on Finanzen.net), "Link" (link to the stock on Finanzen.net), "ISIN", and "WKN". *search_fund* will return a list of dictionaries containing these keys: "Name" (official name), "Fund" (name used on Finanzen.net), "Link" (link to the fund on Finanzen.net), "Manager" (asset manager of fund), "Instrument" (the type of instrument the fund is investing in), "ISIN", and "WKN". *search_etf* offers the following keys: "Name" (official name), "ETF" (name used on Finanzen.net), "Link" (link to the ETF on Finanzen.net), "ISIN", and "WKN". *search_commodity* will only return "Name" (offical name), "Commodity" (name used on Finanzen.net), and "Link" (link to the commodity on Finanzen.net).

## Retrieve Fundamentals
All modules offer functionality to extract fundamentals data for a given instrument. You can use *get_info* for funds, ETFs, and commodities and *get_fundamentals* and *get_estimates* for stocks. All functions take two arguments. The first one ("stock", "etf", fund", or "commodity" respectively) has to be the name used on Finanzen.net. The second one is "output" and has to be equal to either "dict" or "dataframe". Depending on your input, you will receive the data either as a Python dictionary or a Pandas dataframe.

The following information will be returned:

### Stocks
* Quotes
* Key Ratios
* Income Statement
* Balance Sheet
* Other

### Funds
* Fund
* WKN
* ISIN
* Issuer
* Currency
* Premium
* Expense Ratio
* Benchmark
* Volume
* Distribution
* Yearly Performance
* Yearly Volatility
* Capture Ratio
* Batting Average
* Alpha
* Beta
* R2

### ETFs
* ETF
* WKN
* ISIN
* Issuer
* Issue Date
* Instrument Type
* Currency
* Benchmark
* Distribution
* Expense Ratio
* Volume
* Replication

### Commodities
* Commodity
* Value
* Metric

```
stocks.get_fundamentals("lufthansa-aktie")
etfs.get_info("ishares-core-msci-world-etf-ie00b4l5y983")
funds.get_info("schroder-international-selection-fund-inflation-plus-a-lu0107768052")
commodities.get_info("kohlepreis")
```

Alternatively, you could also retrieve that data as a Python dictionary.

```
stocks.get_fundamentals(stock="lufthansa-aktie", output="dict")
etfs.get_info(etf="ishares-core-msci-world-etf-ie00b4l5y983", output="dict")
funds.get_info(fund="schroder-international-selection-fund-inflation-plus-a-lu0107768052", output="dict")
commodities.get_info("kohlepreis", output="dict")
```

For stocks, you can also get estimates on fundamental data.

```
stocks.get_estimates(stock="lufthansa-aktie")
```

## Retrieve Prices
For all instruments you can get the current price on several exchanges. You can use the *get_price* function for that. Here you need to enter the name of the stock, fund, or ETF as the first argument and the name of the stock exchange for which you would like to retrieve the data as the second argument. Currently, the following stock exchanges are supported:

* BER (Berlin)
* BMN (gettex)
* DUS (Düsseldorf)
* FSE (Frankfurt)
* HAM (Hamburg)
* HAN (Hannover)
* MUN (Munich)
* XETRA
* STU (Stuttgart)
* TGT (Tradegate)
* XQTX (Quotrix)
* BAE (Baader Bank)
* NASO (Nasdaq OTC)

Notice that you will receive an error if there is no price for a given instrument on a given stock exchange. By default, the Frankfurt Stock Exchange (FSE) is chosen for you if you don't specify a stock exchange.
Additionally, you can prompt the *get_price* function to return a dictionary or a Pandas dataframe by specifying "dict" or "dataframe" as the third argument.
Commodities don't offer the option to choose a specific exchange. However, for commodities, you need to express the currency you would like to use. The following currencies are supported (always depending on the commodity):
* EUR
* USD
* CHF
* GBP
* MYR

```
stocks.get_price(stock="lufthansa-aktie", exchange="FSE")
etfs.get_price(etf="ishares-core-msci-world-etf-ie00b4l5y983", exchange="FSE")
funds.get_price(fund="schroder-international-selection-fund-inflation-plus-a-lu0107768052", exchange="FSE")
commodities.get_price(commodity="kohlepreis", currency="USD")
```

This will return a single price signal inside a Pandas Dataframe. If you want to receive the price signal inside a Python dictionary, you can set the "output" parameter to "dict".

```
stocks.get_price(stock="lufthansa-aktie", exchange="FSE", output="dict")
etfs.get_price(etf="ishares-core-msci-world-etf-ie00b4l5y983",
	       exchange="FSE", output="dict")
funds.get_price(fund="schroder-international-selection-fund-inflation-plus-a-lu0107768052",
		exchange="FSE", output="dict")
commodities.get_price(commodity="kohlepreis", currency="USD", output="dict")
```

## Disclaimer
Please note that you are free to use this library however you like. However, I do not take any responsibility for financial losses that might result from faulty behavior etc.
