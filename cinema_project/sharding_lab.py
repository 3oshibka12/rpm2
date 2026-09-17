import os
import django
import hashlib
import bisect

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_conf.settings')
django.setup()

from core.models import Ticket, Showtime, Movie, CinemaHall
from django.utils import timezone

TOTAL_RECORDS = 100000

def get_hash(key_string):
    """Детерминированный хэш (MD5 -> int)"""
    return int(hashlib.md5(key_string.encode('utf-8')).hexdigest(), 16)

def get_shard_modulo(key, n):
    return f"shard_{get_hash(key) % n}"

class ConsistentHashRing:
    def __init__(self, nodes, v_nodes=100):
        self.v_nodes = v_nodes
        self.ring = {}
        self.sorted_keys = []
        for node in nodes:
            self.add_node(node)

    def add_node(self, node):
        for i in range(self.v_nodes):
            h = get_hash(f"{node}_vnode_{i}")
            self.ring[h] = node
            bisect.insort(self.sorted_keys, h)

    def get_node(self, key):
        h = get_hash(key)
        idx = bisect.bisect_left(self.sorted_keys, h)
        if idx == len(self.sorted_keys): idx = 0
        return self.ring[self.sorted_keys[idx]]

def setup_reference_data():
    """Создает сеанс в каждом шарде, чтобы работали Foreign Keys"""
    shard_showtimes = {}
    for db in ['shard_0', 'shard_1', 'shard_2', 'shard_3']:
        hall, _ = CinemaHall.objects.using(db).get_or_create(name='Sharded Hall', capacity=100000)
        movie, _ = Movie.objects.using(db).get_or_create(title='Matrix', duration_minutes=120)
        st, _ = Showtime.objects.using(db).get_or_create(movie=movie, hall=hall, start_time=timezone.now())
        shard_showtimes[db] = st
    return shard_showtimes

def main():
    print("=== ПОДГОТОВКА И ЗАГРУЗКА ДАННЫХ ===")
    shard_showtimes = setup_reference_data()
    
    # Очистка шардов перед тестом
    for db in ['shard_0', 'shard_1', 'shard_2']:
        Ticket.objects.using(db).all().delete()
        
    tickets_to_insert = {'shard_0': [], 'shard_1': [], 'shard_2': []}
    emails = [f"user_{i}@example.com" for i in range(TOTAL_RECORDS)]

    print(f"Роутинг {TOTAL_RECORDS} записей по алгоритму hash(key) % 3...")
    for email in emails:
        target_db = get_shard_modulo(email, 3)
        tickets_to_insert[target_db].append(Ticket(
            showtime=shard_showtimes[target_db],
            customer_email=email,
            price=500.00,
            status='PAID'
        ))

    print("Физическая запись в базы данных (bulk_create)...")
    for db, items in tickets_to_insert.items():
        Ticket.objects.using(db).bulk_create(items, batch_size=5000)

    print("\n=== ЧАСТЬ 4. РЕАЛЬНОЕ РАСПРЕДЕЛЕНИЕ ИЗ БД ===")
    for db in ['shard_0', 'shard_1', 'shard_2']:
        count = Ticket.objects.using(db).count()
        print(f"{db} -> {count} записей ({count/TOTAL_RECORDS*100:.2f}%)")

    print("\n=== ЧАСТЬ 5. ИЗМЕНЕНИЕ N (3 -> 4 шардов) ===")
    moved_mod = 0
    for email in emails:
        if get_shard_modulo(email, 3) != get_shard_modulo(email, 4):
            moved_mod += 1
    print(f"hash(key) % N переместит: {moved_mod} записей ({moved_mod/TOTAL_RECORDS*100:.2f}%)")

    print("\n=== ЧАСТЬ 6-7. CONSISTENT HASHING ===")
    ring_3 = ConsistentHashRing(['shard_0', 'shard_1', 'shard_2'])
    ring_4 = ConsistentHashRing(['shard_0', 'shard_1', 'shard_2', 'shard_3'])
    
    moved_cons = 0
    for email in emails:
        if ring_3.get_node(email) != ring_4.get_node(email):
            moved_cons += 1
    print(f"Consistent Hashing переместит: {moved_cons} записей ({moved_cons/TOTAL_RECORDS*100:.2f}%)")

if __name__ == "__main__":
    main()