import mysql.connector
from datetime import datetime
import configparser
import os

# 讀取設定檔
config = configparser.ConfigParser()
config.read('setting.config')

# 從設定檔讀取參數
check_ob = config['check']['check_ob']

# A DB 連線資訊
db_name_A = config['db_a']['db_name']
host_A = config['db_a']['host']
port_A = int(config['db_a']['port'])
user_A = config['db_a']['user']
password_A = config['db_a']['password']

# B DB 連線資訊
db_name_B = config['db_b']['db_name']
host_B = config['db_b']['host']
port_B = int(config['db_b']['port'])
user_B = config['db_b']['user']
password_B = config['db_b']['password']

# 建立輸出資料夾
output_folder = f"diff_{db_name_A}_{db_name_B}"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 要撈的物件 query
if check_ob == 'view':
    query = "select table_schema,table_name from information_schema." + check_ob + "s;"
else:
    query = "select " + check_ob + "_schema," + check_ob + "_name from information_schema." + check_ob + "s;"

# 建立 A 連線
connection = mysql.connector.connect(host=host_A, port=port_A, user=user_A, password=password_A)
cursor = connection.cursor()
cursor.execute(query)
data = cursor.fetchall()
cursor.close()
connection.close()

# 建立 B 連線
connection = mysql.connector.connect(host=host_B, port=port_B, user=user_B, password=password_B)
cursor = connection.cursor()
cursor.execute(query)
data_2 = cursor.fetchall()
cursor.close()
connection.close()

# 將 list 設為 set 來檢查不一樣的
set1 = set(data)
set2 = set(data_2)

diff1 = set1 - set2
diff2 = set2 - set1

# 將結果寫入檔案
output_file = os.path.join(output_folder, f"diff_{check_ob}.txt")
with open(output_file, 'w', encoding='utf-8') as f:
    # 第一部分的差異
    f.write(f"{db_name_A} 有 {db_name_B} 沒有的 {check_ob} 共 {len(diff1)} 個 : \n")
    if diff1:
        formatted_diff1 = ',\n '.join(str(item) for item in sorted(diff1))
        f.write(f"{{\n {formatted_diff1}}}\n")
    else:
        f.write("{}\n")
    
    f.write("#" * 100 + "\n")
    
    # 第二部分的差異
    f.write(f"{db_name_B} 有 {db_name_A} 沒有的 {check_ob} 共 {len(diff2)} 個 : \n")
    if diff2:
        formatted_diff2 = ',\n '.join(str(item) for item in sorted(diff2))
        f.write(f"{{\n {formatted_diff2}}}\n")
    else:
        f.write("{}\n")

print(f"比對結果已輸出至 {output_file}")
