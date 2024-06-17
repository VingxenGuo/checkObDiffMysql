import mysql.connector
from datetime import datetime

# 需要確認差異的物件
check_ob = 'routine' # 不用加 s

# A DB 連線資訊
db_name_A  = 'game-dev' # 此項僅影響輸出名稱，方便結果辨識
host_A = '54.169.249.219'
port_A = 3306
user_A = 'root'
password_A = '!QAZ2wsx'

# B DB 連線資訊
db_name_B = 'kx-merge-s' # 此項僅影響輸出名稱，方便結果辨識
host_B = '35.220.144.182'
port_B = 3306
user_B = 'root'
password_B = ')>x(6isS;9,=}S@:'

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

# 建立 B 連線
connection = mysql.connector.connect(host=host_B, port=port_B, user=user_B, password=password_B)
cursor = connection.cursor()
cursor.execute(query)
data_2 = cursor.fetchall()

# 將 list 設為 set 來檢查不一樣的
set1 = set(data)
set2 = set(data_2)

diff1 = set1 - set2
diff2 = set2 - set1

print(db_name_A, "有", db_name_B, " 沒有的", check_ob, " : ", diff1)
print("#" * 100)
print(db_name_B, "有", db_name_A, " 沒有的", check_ob, " : ", diff2)
