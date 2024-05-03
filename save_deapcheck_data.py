from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime


def setup_driver():
    # Chromeドライバーのセットアップ
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "localhost:9222")  # リモートデバッグポートを指定
    # options.headless = True  # ヘッドレスモードでブラウザを起動
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def sum_dep_by_type(df, start_date, end_date):
    df['DATE'] = pd.to_datetime(df['DATE'])
    filtered_df = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date)]
    return filtered_df.groupby('TYPE')['DEP'].sum()


def save_data_to_csv(df, filename='data.csv'):
    # DataFrameをCSVファイルに保存
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


def get_data_from_pages(base_url):
    driver = setup_driver()
    all_data = pd.DataFrame()

    for i in range(1, 108):
        url = base_url + str(i)
        print(url)
        driver.get(url)
        rows = driver.find_elements(By.CSS_SELECTOR, 'table.c-table.-history tr')[1:]  # ヘッダーを除外
        data = []
        for i, row in enumerate(rows):
            cols = row.find_elements(By.CLASS_NAME, 'data')
            date = cols[0].text.strip()
            type_ = cols[1].text.strip().replace('\n', '')
            dep = float(cols[2].text.strip())
            data.append({'DATE': date, 'TYPE': type_, 'DEP': dep})
            if i == 4:
                break

        page_data = pd.DataFrame(data)
        all_data = pd.concat([all_data, page_data], ignore_index=True)

    driver.quit()
    return all_data


# すべてのページからデータを取得
base_url = "https://game-jtcb.playmining.com/scholar_ship/member/detail?q_page=1&l_page=1&p_page=1&id=37558&sort=1&sort_key=get_at&q_sort=1&q_sort_key=get_at&l_sort=1&l_sort_key=get_at&p_sort=1&p_sort_key=get_at&page="
data_df = get_data_from_pages(base_url)
save_data_to_csv(data_df)
# 期間指定（例：2024年4月23日から2024年4月23日）
start_date = datetime(2024, 4, 10)
end_date = datetime(2024, 4, 23)
summed_deps = sum_dep_by_type(data_df, start_date, end_date)

print(summed_deps)
