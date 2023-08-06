import json
import random
import pandas as pd
import numpy as np
import requests
import os
import time
import datetime

import openpyxl
from pytesseract import pytesseract
import cv2
from pdf2image import convert_from_path

def contrast(img):
    brightness = -50
    contrast = 100
    img = np.int16(img)
    img = img * (contrast / 127 + 1) - contrast + brightness
    img = np.clip(img, 0, 255)
    img = np.uint8(img)
    return img

def crop(image):
    dimensions = image.shape
    crop_img = image[725:dimensions[0], 0:dimensions[1]]
    return crop_img

def length_stock_name(string):
    flag = False
    i = 0
    index = 0
    index_start = 0
    while i < len(string):
        if not flag:
            if string[i].isdigit() or string[i] == "." or string[i] == " " or string[i] == ",":
                i = i + 1
            else:
                flag = True
                index_start = i
                i = i + 1
        elif flag:
            if string[i].isdigit():
                index = i
                break
            else:
                i = i + 1
    return index_start, index

def line_parser(rest):
    print(rest)
    new_equity_str = []
    index = 0
    count = 0
    add = 1
    while count < 4 and len(rest) > 0:
        add = 1
        if count == 3:
            if rest[-1:] == "-":
                new_equity_str.append(str("-"+(rest[0:len(rest)-4] + "." + rest[len(rest)-3:]).strip().rstrip("-").lstrip(".").replace(" .", ".").replace(". ", ".").replace("..",".")))
            else:
                new_equity_str.append(str((rest[0:len(rest) - 3] + "." + rest[len(rest) - 2:]).strip().lstrip(".").replace(" .",".").replace(". ", ".").replace("..",".")))
            break

        match_dot = rest[index:].find(".")
        match_comma = rest[index:].find(",")
        match_space = rest[index:].find(" ")
        list_match = [match_dot,match_comma,match_space]
        list_match_pos = [i for i in list_match if i >=0]
        try:
            match = min(list_match_pos)
        except:
            break
        match1 = index + match
        if rest[match1 + 3:match1 + 4] == " ":
            new_equity_str.append(str(rest[0:match1] + "." + rest[match1 + 1:match1 + 3]).strip().lstrip(".").replace(" .", ".").replace(". ", ".").replace("..","."))
            count = count + 1
            add = 3
            rest = rest[match1+3:]
            index = 0
        elif (rest[match1 + 3:match1 + 6] == "06 " or rest[match1 + 3:match1 + 6] == "00 " or rest[match1 + 4:match1 + 6] == "0 "or rest[match1 + 4:match1 + 6] == "6 ") and count == 1:
            new_equity_str.append(str(rest[0:match1] + "." + rest[match1 + 1:match1 + 5]).strip().lstrip(".").replace(" .", ".").replace(". ", ".").replace("..","."))
            count = count + 1
            add = 5
            rest = rest[match1+5:]
            index = 0
        elif rest[match1 + 3:match1 + 4] == "-":
            new_equity_str.append(str("-" + rest[0:match1] + "." + rest[match1 + 1:match1 + 3]).strip().lstrip(".").replace(" .", ".").replace(". ", ".").replace("..","."))
            count = count + 1
            add = 3
            rest = rest[match1+3:]
            index = 0
        else:
            index = index+match+1
    return new_equity_str

def parse_report(text):
    equities = text.split("\n")

    for i in range(len(equities)):
        new_equity_str = ""
        stock_name_start = length_stock_name(equities[i])[0]
        stock_name_end = length_stock_name(equities[i])[1]
        new_equity_str = equities[i].replace(" .", ".")
        new_equity_str = [equities[i][0:stock_name_start].strip().replace(",0000",".0000").replace(",","")]+[equities[i][stock_name_start:stock_name_end]]

        rest = str(equities[i][stock_name_end:])
        new_equity_str = new_equity_str + line_parser(rest)
        for j in range(len(new_equity_str)):
            new_equity_str[j] = new_equity_str[j].strip().replace(",","")
        equities[i] = new_equity_str
    for thing in equities:
        print(thing)

    df = pd.DataFrame(equities, columns=['Shares', 'Security', 'Cost', 'Price', 'Market Value', 'Unrealized Gain/Loss'])
    df = df.dropna()
    df['Shares'] = pd.to_numeric(df['Shares'])
    df['Security'] = df['Security'].astype(str)
    df['Cost'] = df['Cost'].astype(float)
    df['Price'] = df['Price'].astype(float)
    df['Market Value'] = df['Market Value'].astype(float)
    df['Unrealized Gain/Loss'] = df['Unrealized Gain/Loss'].astype(float)
    return df

def mellon_scraper(pdfs_path,images_path,output_path,tesseract_path):
    year = input("year?\n")
    pdfs_path = os.path.join(pdfs_path,str(year))
    pdfs = sorted(os.listdir(pdfs_path))

    for pdf in pdfs:
        if pdf == '.DS_Store':
            continue
        else:
            parent_dir = os.path.join(images_path,str(year))
            path = pdf
            if os.path.isdir(parent_dir):
                print("Directory already exists")
                if not os.path.isdir(os.path.join(parent_dir,path)):
                    os.mkdir(os.path.join(parent_dir,path))
                output_folder = os.path.join(parent_dir, path)
            else:
                os.mkdir(parent_dir)
                os.mkdir(os.path.join(parent_dir,path))
                output_folder = os.path.join(parent_dir, path)

            pages = convert_from_path(os.path.join(pdfs_path,path), 350)
            i = 1
            for page in pages:
                image_name = pdf.rstrip('.pdf') + " Page_" + str(i) + ".jpg"
                page.save(os.path.join(output_folder,image_name),"JPEG", dpi =(1000,1000))
                i = i+1

        jpegs = sorted(os.listdir(output_folder))
        text_all = ""
        path_to_tesseract = tesseract_path
        pytesseract.tesseract_cmd = path_to_tesseract
        count = 0
        for jpeg in jpegs:
            count = count +1
            file = os.path.join(parent_dir,pdf,jpeg)
            print(file)
            # load the original image
            img = cv2.imread(file)
            lower_black = np.array([0, 0, 0], dtype="uint16")
            upper_black = np.array([200, 200, 200], dtype="uint16")
            img = cv2.inRange(img, lower_black, upper_black)
            th, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
            img = cv2.bitwise_not(crop(contrast(img)))
            # pytesseract image to string to get results
            text = str(pytesseract.image_to_string(img, config='-c tessedit_char_whitelist="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ., -&",  --psm 6'))
            text_all = text_all + text + "\n"
        start_word = 'INVESTMENTS EQUITY'
        end_word = 'TOTAL INVESTMENT'
        start = text_all.find(start_word)
        clean = text_all[start+len(start_word):].strip()
        end = clean.find(end_word)
        clean = clean[:end].strip()
        data = parse_report(clean)
        output_path_ = output_path+str(year)+".xlsx"

        try:
            if os.path.exists(output_path_):
                with pd.ExcelWriter(output_path_,mode="a",engine='openpyxl') as writer:
                    writer.book = openpyxl.load_workbook(output_path_)
                    data.to_excel(writer, sheet_name=pdf.rstrip(".pdf"))
            else:
                data.to_excel(output_path_, sheet_name=pdf.rstrip(".pdf"))
        except:
            continue

benchmarks = {
    "TECH":"SP500-45",
    "HEAL":"HCX",
    "COMM":"SP500-50",
    "STAP":"SP500-30",
    "DISC":"SP500-25",
    "INDU":"SP500-20",
    "UTIL":"SP500-55",
    "ENER":"SP500-10",
    "REAL":"SP500-60",
    "MATE":"SP500-15",
    "FINA":"SP500-40"
}

benchmark_sectors_old = {
    "CONS": ["STAP", "DISC"],
    "ENER": ["ENER"],
    "FINA": ["FINA", "REAL"],
    "HEAL": ["HEAL"],
    "TECH": ["TECH","COMM"],
    "INDU": ["INDU", "UTIL", "MATE"],
}
benchmark_sectors_new_2020_2H = {
    "CONS": ["STAP", "DISC"],
    "ENER": ["ENER"],
    "FINA": ["FINA","REAL"],
    "HEAL": ["HEAL"],
    "TECH": ["TECH"],
    "INDU": ["INDU","UTIL","MATE"],
    "COMM": ["COMM"]
}
benchmark_sectors_new_2021 = {
    "TECH": ["TECH"],
    "COMM": ["COMM"],
    "HEAL": ["HEAL"],
    "CONS": ["STAP", "DISC"],
    "INDU": ["INDU","MATE"],
    "ENER": ["ENER","UTIL"],
    "FINA": ["FINA","REAL"]
}
benchmark_sectors_new_2022 = {
    "TECH": ["TECH"],
    "COMM": ["COMM"],
    "HEAL": ["HEAL"],
    "STAP": ["STAP"],
    "DISC": ["DISC"],
    "INDU": ["INDU","MATE"],
    "ENER": ["ENER","UTIL"],
    "FINA": ["FINA","REAL"]
}

years = ["2011","2012",'2013','2014','2015','2016','2017','2018','2019','2020','2021']
months = ['Jan','Feb','Mar',"Apr",'May','Jun',"Jul",'Aug','Sep',"Oct",'Nov','Dec']
real_estate_start = "9/30/16"

def get_weight(df, spx, year):
    df["Year"] = df["Year"].astype(str)
    spx["Year"] = spx["Year"].astype(str)
    idx = df.index[df['Year'] == year].tolist()
    idx.insert(0,idx[0]-1)
    df = df.iloc[idx]["Market Cap"]
    idx_s = spx.index[spx['Year'] == year].tolist()
    idx_s.insert(0, idx_s[0] - 1)
    spx = spx.iloc[idx_s]["Market Cap"]
    weights = {}
    count = idx_s[0]
    for month in months:
        weights[month] = df[count]/spx[count]
        count = count + 1
    return weights

def get_perf(df,spx,year):
    df["Year"] = df["Year"].astype(str)
    idx = df.index[df['Year'] == year].tolist()
    idx.insert(0, idx[0] - 1)
    df = df.iloc[idx]["Index Value"]
    returns = {}
    spx["Year"] = spx["Year"].astype(str)
    idx_s = spx.index[spx['Year'] == year].tolist()
    idx_s.insert(0, idx_s[0] - 1)
    spx = spx.iloc[idx_s]["Index Value"]
    returns_spx = {}
    count = idx[0]
    for month in months:
        if df[count] != 0:
            returns[month] = df[count+1]/df[count]-1
        else:
            returns[month] = 0
        returns_spx[month] = spx[count+1]/spx[count]-1
        count = count + 1

    return [returns, returns_spx]

def benchmark(benchmark_data_path):
    if os.path.isfile(benchmark_data_path):
        year = input("year:\n")
        while year != "end":
            if year not in years:
                year = input("year invalid. reenter year or end:\n")
                continue
            else:
                bench_perf = [months]
                weight_all = [months]
                for benchmark in benchmarks:
                    if benchmark == "SPX":
                        continue
                    spx = pd.read_excel(benchmark_data_path,sheet_name="^SPX")
                    df = pd.read_excel(benchmark_data_path,sheet_name="^"+benchmarks[benchmark])
                    weights = get_weight(df,spx,year)
                    returns_2 = get_perf(df,spx,year)
                    returns = returns_2[0]
                    returns_spx = returns_2[1]
                    weighted_returns = [weights[month]*returns[month] for month in weights]
                    bench_perf.append(weighted_returns)
                    weight_all.append(list(weights.values()))
                bench_df = pd.DataFrame(np.transpose(bench_perf), columns = ["Month"]+list(benchmarks.keys())[0:])
                weight_df = pd.DataFrame(np.transpose(weight_all),columns=["Month"]+list(benchmarks.keys())[0:])
                match int(year):
                    case 2022:
                        print(year)
                        benchmark_sectors = benchmark_sectors_new_2022
                        bench_perf_sector = [months]
                        weight_sector = [months]
                        for sector in benchmark_sectors:
                            if sector == "GSPC":
                                continue
                            else:
                                sum_weighted_returns = [0.0] * 12
                                sum_weights = [0.0] * 12
                                for i in benchmark_sectors[sector]:
                                    sum_weighted_returns = [sum_weighted_returns[j] + float(list(bench_df[i])[j]) for j in
                                                            range(len(list(bench_df[i])))]
                                    sum_weights = [sum_weights[j] + float(list(weight_df[i])[j]) for j in
                                                   range(len(list(weight_df[i])))]
                                bench_perf_sector.append(sum_weighted_returns)
                                weight_sector.append(sum_weights)
                        bench_sector_df = pd.DataFrame(np.transpose(bench_perf_sector),columns=["Month"] + list(benchmark_sectors_old.keys())[0:])
                        weight_sector_df = pd.DataFrame(np.transpose(weight_sector),columns=["Month"] + list(benchmark_sectors_old.keys())[0:])
                        for col in weight_sector_df:
                            if col == "Month":
                                continue
                            weight_sector_df[col] = weight_sector_df[col].astype(float).rdiv(1)
                            bench_sector_df[col] = bench_sector_df[col].astype(float) * weight_sector_df[col]
                        print(bench_sector_df)
                        print(returns_spx)
                    case 2021:
                        print(year)
                        benchmark_sectors = benchmark_sectors_new_2021
                        bench_perf_sector = [months]
                        weight_sector = [months]
                        for sector in benchmark_sectors:
                            if sector == "GSPC":
                                continue
                            else:
                                sum_weighted_returns = [0.0] * 12
                                sum_weights = [0.0] * 12
                                for i in benchmark_sectors[sector]:
                                    sum_weighted_returns = [sum_weighted_returns[j] + float(list(bench_df[i])[j]) for j in
                                                            range(len(list(bench_df[i])))]
                                    sum_weights = [sum_weights[j] + float(list(weight_df[i])[j]) for j in
                                                   range(len(list(weight_df[i])))]
                                bench_perf_sector.append(sum_weighted_returns)
                                weight_sector.append(sum_weights)
                        bench_sector_df = pd.DataFrame(np.transpose(bench_perf_sector),columns=["Month"] + list(benchmark_sectors_old.keys())[0:])
                        weight_sector_df = pd.DataFrame(np.transpose(weight_sector),columns=["Month"] + list(benchmark_sectors_old.keys())[0:])
                        for col in weight_sector_df:
                            if col == "Month":
                                continue
                            weight_sector_df[col] = weight_sector_df[col].astype(float).rdiv(1)
                            bench_sector_df[col] = bench_sector_df[col].astype(float) * weight_sector_df[col]
                        print(bench_sector_df)
                        print(returns_spx)
                    case 2020:
                        print(year)
                        benchmark_sectors = benchmark_sectors_new_2020_2H
                        bench_perf_sector = [months]
                        weight_sector = [months]
                        for sector in benchmark_sectors:
                            if sector == "GSPC":
                                continue
                            else:
                                sum_weighted_returns = [0.0] * 12
                                sum_weights = [0.0] * 12
                                for i in benchmark_sectors[sector]:
                                    sum_weighted_returns = [sum_weighted_returns[j] + float(list(bench_df[i])[j]) for j in
                                                            range(len(list(bench_df[i])))]
                                    sum_weights = [sum_weights[j] + float(list(weight_df[i])[j]) for j in
                                                   range(len(list(weight_df[i])))]
                                bench_perf_sector.append(sum_weighted_returns)
                                weight_sector.append(sum_weights)
                        bench_sector_df = pd.DataFrame(np.transpose(bench_perf_sector),columns=["Month"] + list(benchmark_sectors.keys())[0:])
                        weight_sector_df = pd.DataFrame(np.transpose(weight_sector),columns=["Month"] + list(benchmark_sectors.keys())[0:])
                        for col in weight_sector_df:
                            if col == "Month":
                                continue
                            weight_sector_df[col] = weight_sector_df[col].astype(float).rdiv(1)
                            bench_sector_df[col] = bench_sector_df[col].astype(float) * weight_sector_df[col]
                        print(bench_sector_df)
                        print(returns_spx)
                    case _:
                        print(year)
                        benchmark_sectors = benchmark_sectors_old
                        bench_perf_sector = [months]
                        weight_sector = [months]
                        for sector in benchmark_sectors:
                            if sector == "GSPC":
                                continue
                            else:
                                sum_weighted_returns = [0.0]*12
                                sum_weights = [0.0] * 12
                                for i in benchmark_sectors[sector]:
                                    sum_weighted_returns = [sum_weighted_returns[j] + float(list(bench_df[i])[j]) for j in range(len(list(bench_df[i])))]
                                    sum_weights = [sum_weights[j]+float(list(weight_df[i])[j]) for j in range(len(list(weight_df[i])))]
                                bench_perf_sector.append(sum_weighted_returns)
                                weight_sector.append(sum_weights)
                        bench_sector_df = pd.DataFrame(np.transpose(bench_perf_sector), columns=["Month"] + list(benchmark_sectors_old.keys())[0:])
                        weight_sector_df = pd.DataFrame(np.transpose(weight_sector), columns=["Month"] + list(benchmark_sectors_old.keys())[0:])
                        for col in weight_sector_df:
                            if col == "Month":
                                continue
                            weight_sector_df[col] = weight_sector_df[col].astype(float).rdiv(1)
                            bench_sector_df[col] = bench_sector_df[col].astype(float)*weight_sector_df[col]
                        print(bench_sector_df)
                        print(returns_spx)
            year = input("year (enter end to stop program):\n")
    else:
        print("Directory does not exist.")
def pull_div_history(stock,asset):
    print('hello')
    url = "https://api.nasdaq.com/api/quote/" + str(stock) + "/dividends?assetclass="+str(asset)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
        "Upgrade-Insecure-Requests": "1", "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
    r = requests.get(url, headers=headers)
    data = r.text
    dividend_dict = json.loads(data)
    print("from nasdaq.com:\n", dividend_dict)
    return dividend_dict

def save_div_history(tickers,asset,dividend_path,update=bool):
    match asset:
        case "stocks":
            print("hello")
            for stock in tickers:
                if update:
                    dividend_dict = pull_div_history(stock,"stocks")
                    with open(os.path.join(dividend_path,stock + "-dividend-history.csv"), "w") as output_file:
                        json.dump(dividend_dict, output_file)
                    time.sleep(random.randrange(30))
                else:
                    if os.path.isdir(os.path.join(dividend_path,stock+"-dividend-history.csv")):
                        continue
                    else:
                        dividend_dict = pull_div_history(stock, "stocks")
                        with open(os.path.join(dividend_path, stock + "-dividend-history.csv"), "w") as output_file:
                            json.dump(dividend_dict, output_file)
                    time.sleep(random.randrange(30))
        case "etf":
            for stock in tickers:
                if update:
                    dividend_dict = pull_div_history(stock, "etf")
                    with open(os.path.join(dividend_path, stock + "-dividend-history.csv"), "w") as output_file:
                        json.dump(dividend_dict, output_file)
                    time.sleep(random.randrange(30))
                else:
                    if os.path.isdir(stock + "-dividend-history.csv"):
                        continue
                    else:
                        dividend_dict = pull_div_history(stock, "etf")
                        with open(os.path.join(dividend_path, stock + "-dividend-history.csv"), "w") as output_file:
                            json.dump(dividend_dict, output_file)
                    time.sleep(random.randrange(30))
                time.sleep(random.randrange(30))

def get_div_history(ticker,asset,dividend_path, startdate,enddate):
    path = str(os.path.join(dividend_path,str(ticker+"-dividend-history.csv")))
    if os.path.isfile(path):
        data = open(os.path.join(dividend_path,str(ticker+"-dividend-history.csv")),"r")
        with data as input_file:
            dividend_dict = json.load(input_file)
        try:
            columns = list(dividend_dict['data']['dividends']['headers'].values())
            rows = [list(i.values()) for i in dividend_dict['data']['dividends']['rows']]
            df = pd.DataFrame(rows, columns=columns)
            df['Ex/EFF DATE'] = np.where(df['Ex/EFF DATE'] == 'N/A', df['PAYMENT DATE'],df['Ex/EFF DATE'])
            df['Ex/EFF DATE'] = pd.to_datetime(df['Ex/EFF DATE'])
            idx = df.index[df['Ex/EFF DATE'] >= startdate].intersection(df.index[df['Ex/EFF DATE'] <= enddate]).tolist()
            df = df.iloc[idx]
            df_format = df[["Ex/EFF DATE","PAYMENT DATE","CASH AMOUNT"]]
            return df_format
        except:
            return dividend_dict['message']
    else:
        print("hi")
        tickers = [ticker]
        print(ticker)
        save_div_history(tickers, asset,dividend_path,True)
           
