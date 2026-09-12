import datetime
import os
import psycopg2

STATE_FILE = 'alert_state.txt'

DB_CONFIG = {
    'dbname': 'cinema_db',
    'user': 'cinema_user',
    'password': 'cinema_password',
    'host': 'localhost',
    'port': '5433'
}

def send_alert(message, is_recovery=False):
    is_failing = os.path.exists(STATE_FILE)
    if not is_recovery and not is_failing:
        print(f"\n🔴 [CRITICAL ALERT] -> {message}")
        with open(STATE_FILE, 'w') as f: f.write('failed')
    elif not is_recovery and is_failing:
        print("\n🟡 [SUPPRESSED ALERT] -> Ошибка повторяется, алерт заглушен.")
    elif is_recovery and is_failing:
        print(f"\n🟢 [RECOVERY ALERT] -> {message}")
        os.remove(STATE_FILE)

def add_months(year, month, n):
    m = month + n - 1
    return year + m // 12, m % 12 + 1

def run_job():
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{now_str}")
    print("Partition job started.")
    
    today = datetime.date.today()
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()

        required = []
        for i in range(4):
            ty, tm = add_months(today.year, today.month, i)
            ny, nm = add_months(ty, tm, 1)
            required.append({
                'name': f"core_ticket_{ty}_{tm:02d}",
                'from': f"{ty}-{tm:02d}-01",
                'to': f"{ny}-{nm:02d}-01"
            })

        existing_count = 0
        missing = []
        for req in required:
            cursor.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = %s);", (req['name'],))
            if cursor.fetchone()[0]:
                existing_count += 1
            else:
                missing.append(req)

        print(f"Existing partitions: {existing_count}")
        print(f"Required partitions: {len(required)}")
        print(f"Missing partitions: {len(missing)}")

        if missing:
            for req in missing:
                print(f"Creating: {req['name']}")
                sql = f"CREATE TABLE {req['name']} PARTITION OF core_ticket FOR VALUES FROM ('{req['from']}') TO ('{req['to']}');"
                cursor.execute(sql)
            
            print("Partition created successfully.")
            
        print("Partition job finished.")
        
        if os.path.exists(STATE_FILE):
            send_alert("Partition check OK. All required partitions exist.", is_recovery=True)

        conn.close()

    except Exception as e:
        print("\nJob Failed!")
        print(f"Error: {e}")
        send_alert(f"Missing partitions or DB failure! Database error: {str(e).strip()}")

if __name__ == "__main__":
    run_job()