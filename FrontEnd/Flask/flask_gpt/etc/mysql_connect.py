import pymysql

# MySQL 서버 연결 설정
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "destiny2_db"
}

# 연결 생성
conn = pymysql.connect(**db_config)

# 커서 생성
cursor = conn.cursor()

# SQL 쿼리 실행
query = """SELECT * FROM all_date_timestamp
            WHERE description LIKE '%Lisbon-13%' """
cursor.execute(query)

# 결과 가져오기
results = cursor.fetchall()

count = 0
# 결과 출력
for row in results:
    print(row)
    print(type(row))
    count += 1
    
print(count)
print(type(results))

# 연결 및 커서 닫기
cursor.close()
conn.close()
