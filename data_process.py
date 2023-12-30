import requests
import json
import pandas as pd
import matplotlib.pyplot as plt


# The API endpoint for the POST request
url = "https://v1.cn-abs.com/ajax/ChartMarketHandler.ashx"

# Headers
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "v1.cn-abs.com",
    "Origin": "https://v1.cn-abs.com",
    "Referer": "https://v1.cn-abs.com/",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
}

# Payload for the POST request
payload = {    
    'type': 'monthlyIssuance' # 最近两年产品发行金额统计
}


def fetch_data(url, headers, data):
    """
    Fetches data from the URL using a POST request.
    
    Args:
        url (str): The URL to which the POST request is made.
        headers (dict): Headers to include in the request.
        data (dict): Data to send in the body of the POST request.
        
    Returns:
        The response from the server.
    """
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        # Assuming the response's content is JSON, parse and return it.
        # If the response is in another format, this line will need to change.
        res = response.json()
        return res
    else:
        print("Failed to retrieve content, status code:", response.status_code)
        return None


def main(data):
    # Fetch and process data from the API
    response = fetch_data(url, headers, data)
    
    if response is not None:
        print("Response from server:", response)
        # Further processing can be done here depending on the structure of response
    return response


def data_parse(data):
    """
    Parses the given data and returns a list of dictionaries.
    
    Args:
        data (list): A list of dictionaries containing data to be parsed.
        
    Returns:
        list: A list of dictionaries where each dictionary represents a year and its corresponding data.
    """
    res = []
    for item in data:
        # print(item)
        year = item['SeriesName']
        # print('year: ', year)
        year_data = {'year': year}
        for point in item['Points']:
            month = point['X']
            value = point['Y']
            # print('month: ', month)
            # print('value: ', value)
            year_data[month] = value
        res.append(year_data)
        
    return res


def data2df(data):
    """
    Convert list of dictionaries to DataFrame.

    Parameters:
    - data (list): A list of dictionaries containing the data.

    Returns:
    - df (DataFrame): The transposed DataFrame with months as rows and years as columns.
    """
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)
    # Transpose the DataFrame to make months the rows and years the columns
    df = df.set_index('year').transpose()
    return df


def save_to_csv(df, fileName):
    """
    Save DataFrame to CSV file.

    Parameters:
    - df (DataFrame): The DataFrame to be saved.

    Returns:
    - None
    """
    # Save DataFrame to CSV file
    df.to_csv('./data/{}.csv'.format(fileName))


def visualization(df):
    """
    Visualizes the data in a line plot.

    Parameters:
    - df: The data to be visualized. It should be a pandas DataFrame.

    Returns:
    None
    """
    # Visualizing the data
    plt.figure(figsize=(12, 6))
    plt.plot(df, marker='o')
    plt.title('Product issuance amount statistics in the last two years')
    plt.xlabel('Month')
    plt.ylabel('Issue amount (billion)')
    plt.grid(True)
    plt.legend(df.columns)
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.show()


if __name__ == '__main__':
    payload = {    
        'type': 'monthlyIssuance' # 最近两年产品发行金额统计
    }
    data = main(data=payload)
    print(data)

    data = data_parse(data)
    print(data)

    df = data2df(data)
    print(df)

    visualization(df)

    file_name = 'monthly_issuance'
    save_to_csv(df, file_name)