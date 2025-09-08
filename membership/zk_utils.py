from zk import ZK, const

def get_connection():
    """Connect to ZKTeco K50 device."""
    zk = ZK('192.168.18.201', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    conn = zk.connect()
    return conn
