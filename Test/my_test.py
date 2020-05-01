from app.networking import get_first_name, get_last_name , get_email, get_phone_number, create_contact, reading_from_sheet, writing_to_sheet
import os, pytest, gspread


def test_to_usd():
    assert to_usd(4.50) == "$4.50" #Adds the Dollaer
    assert to_usd(4.5) == "$4.50" #Has two decimal places
    assert to_usd(4.5555555) == "$4.56" #should round to two decimal places
    assert to_usd(123456789.5555) == "$123,456,789.56" # should display thousand separators
def test_get_response():
    symbol = "NFLX"

    parsed_response = get_response(symbol)

    assert isinstance(parsed_response, dict)#Tests that the parsed_response is of the class "dict"
    assert "Meta Data" in parsed_response.keys() #Tests that one of the "keys" in the parsed_response dictionary is "Meta Data"
    assert "Time Series (Daily)" in parsed_response.keys()#Tests that one of the "keys" in the parsed_response dictionary is "Time Series (Daily)"
    assert parsed_response["Meta Data"]["2. Symbol"] == symbol#Tests that "symbol" variable in the parsed response data has the same value as the one given as a parameter
def test_transform_response():
    parsed_response = {
        "Meta Data": {
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "MSFT",
            "3. Last Refreshed": "2018-06-08",
            "4. Output Size": "Full size",
            "5. Time Zone": "US/Eastern"
        },
        "Time Series (Daily)": {
            "2019-06-08": {
                "1. open": "101.0924",
                "2. high": "101.9500",
                "3. low": "100.5400",
                "4. close": "101.6300",
                "5. volume": "22165128"
            },
            "2019-06-07": {
                "1. open": "102.6500",
                "2. high": "102.6900",
                "3. low": "100.3800",
                "4. close": "100.8800",
                "5. volume": "28232197"
            },
            "2019-06-06": {
                "1. open": "102.4800",
                "2. high": "102.6000",
                "3. low": "101.9000",
                "4. close": "102.4900",
                "5. volume": "21122917"
            }
        }
    }

    transformed_response = [
        {"timestamp": "2019-06-08", "open": 101.0924, "high": 101.95, "low": 100.54, "close": 101.63, "volume": 22165128},
        {"timestamp": "2019-06-07", "open": 102.65, "high": 102.69, "low": 100.38, "close": 100.88, "volume": 28232197},
        {"timestamp": "2019-06-06", "open": 102.48, "high": 102.60, "low": 101.90, "close": 102.49, "volume": 21122917},
    ]

    assert transform_response(parsed_response) == transformed_response #Tests that the function "transform_response" changes the parameter "parsed_response" correctly
def test_write_to_csv():
    example_rows = [
        {"timestamp": "2019-06-08", "open": "101.0924", "high": "101.9500", "low": "100.5400", "close": "101.6300", "volume": "22165128"},
        {"timestamp": "2019-06-07", "open": "102.6500", "high": "102.6900", "low": "100.3800", "close": "100.8800", "volume": "28232197"},
        {"timestamp": "2019-06-06", "open": "102.4800", "high": "102.6000", "low": "101.9000", "close": "102.4900", "volume": "21122917"},
        {"timestamp": "2019-06-05", "open": "102.0000", "high": "102.3300", "low": "101.5300", "close": "102.1900", "volume": "23514402"},
        {"timestamp": "2019-06-04", "open": "101.2600", "high": "101.8600", "low": "100.8510", "close": "101.6700", "volume": "27281623"},
        {"timestamp": "2019-06-01", "open": '99.2798',  "high": "100.8600", "low": "99.1700",  "close": "100.7900", "volume": "28655624"}
    ]
    
    csv_file_path = os.path.join(os.path.dirname(__file__), "example_reports", "temp_prices.csv")
    
    if os.path.isfile(csv_file_path):
        os.remove(csv_file_path)
    
    assert os.path.isfile(csv_file_path) == False # just making sure the test was setup properly(AKA removes filepath and deletes file temp_prices.csv)
    
    # INVOCATION
    
    result = write_to_csv(example_rows, csv_file_path)
    
    # EXPECTATIONS
    
    assert result == True #If the function invokes correctly, it should return "True" 
    assert os.path.isfile(csv_file_path) == True #Checks if a .csv file was created at the location of the csv_file_path
    
    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
    with open(csv_file_path, "r") as csv_file: # "r" means "open the file for reading"
        reader = csv.DictReader(csv_file) # assuming your CSV has headers
        for row in reader:
            assert row["timestamp"] == "2019-06-08" #Checks to see if the value of first timestamp is correct
            assert row["open"] == "101.0924" #Checks to see if the value of first open price is correct
            break
    with open(csv_file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file) 
        x = 0 
        for row in reader:
            x +=1
        row_number = len(example_rows)
        assert x == row_number #Checks to see if the .csv file has all the rows
def test_get_recent_high():
    dates = [
        {"timestamp": "2019-06-08", "open": "101.0924", "high": "101.9500", "low": "100.5400", "close": "101.6300", "volume": "22165128"},
        {"timestamp": "2019-06-07", "open": "102.6500", "high": "102.6900", "low": "100.3800", "close": "100.8800", "volume": "28232197"},
        {"timestamp": "2019-06-06", "open": "102.4800", "high": "102.6000", "low": "101.9000", "close": "102.4900", "volume": "21122917"},
        {"timestamp": "2019-06-05", "open": "102.0000", "high": "102.3300", "low": "101.5300", "close": "102.1900", "volume": "23514402"},
        {"timestamp": "2019-06-04", "open": "101.2600", "high": "101.8600", "low": "100.8510", "close": "101.6700", "volume": "27281623"},
        {"timestamp": "2019-06-01", "open": '99.2798',  "high": "100.8600", "low": "99.1700",  "close": "100.7900", "volume": "28655624"}
        ]
    recent_high = get_recent_high(dates)

    assert recent_high == 102.6900 #Checks to see if recent_high function operating properly
    
    