from datetime import datetime

# 获取当前日期和时间
now = datetime.now()

# 使用strftime进行格式化
date_str = now.strftime("%Y-%m-%d")

print("Date:", date_str)
