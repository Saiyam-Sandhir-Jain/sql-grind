import time
from sqlalchemy import create_engine, MetaData, Table, select, text
from sqlalchemy.pool import QueuePool, NullPool
from config import DATABASE_URL

# ============================================================
# 1. CONFIGURE CUSTOM CONNECTION POOL
# ============================================================
# Default pool class for PostgreSQL engines is QueuePoolimport time
from sqlalchemy import create_engine, MetaData, Table, select, text
from sqlalchemy.pool import QueuePool, NullPool
from config import DATABASE_URL

# ============================================================
# 1. CONFIGURE CUSTOM CONNECTION POOL
# ============================================================
# Default pool class for PostgreSQL engines is QueuePool
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,          # Maintain up to 5 steady-state connections
    max_overflow=10,      # Allow up to 10 additional temporary connections
    pool_timeout=30,      # Wait up to 30 seconds before throwing TimeoutError
    pool_recycle=1800,    # Recycle connections after 30 minutes (1800 seconds)
    pool_pre_ping=True,   # "Pre-ping" connection with 'SELECT 1' to ensure it's alive
)

metadata = MetaData()
employee = Table("employee", metadata, autoload_with=engine)


def print_pool_status(engine, label=""):
    """Utility to print current pool checkout metrics."""
    pool = engine.pool
    print(f"[{label}] Pool Status -> Size: {pool.size()} | Checked out: {pool.checkedout()} | Overflow: {pool.overflow()}")


# ============================================================
# 2. CHECKOUT & CHECKIN DEMONSTRATION
# ============================================================
def demo_pool_lifecycle():
    print("\n--- 1. Connection Checkout & Checkin ---")
    print_pool_status(engine, "Initial")

    # Checking out Connection 1
    with engine.connect() as conn1:
        print_pool_status(engine, "Conn 1 Checked Out")

        # Checking out Connection 2 concurrently
        with engine.connect() as conn2:
            print_pool_status(engine, "Conn 1 & 2 Checked Out")
            
            # Perform query on active connection
            res = conn2.execute(select(employee.c.name).limit(1)).scalar()
            print(f"Query Result: {res}")

    # Both connections returned to pool upon exiting context blocks
    print_pool_status(engine, "After Return to Pool")


# ============================================================
# 3. ADVANCED POOL CONFIGURATIONS
# ============================================================
def demo_null_pool():
    print("\n--- 2. NullPool (Disabling Pooling for Serverless/Short-lived Tasks) ---")
    
    # NullPool opens a fresh database connection every time and closes it immediately
    # Useful for AWS Lambda, serverless tasks, or when using external proxies like PgBouncer
    null_engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,
    )

    with null_engine.connect() as conn:
        result = conn.execute(text("SELECT pg_backend_pid()")).scalar()
        print(f"NullPool Execution Backend PID: {result}")
    
    null_engine.dispose()


# ============================================================
# 4. DISPOSING THE POOL
# ============================================================
def demo_engine_dispose():
    print("\n--- 3. Engine Disposal & Cleanup ---")
    print_pool_status(engine, "Before Dispose")

    # Closes all idle connections in the pool.
    # New checkouts will recreate connections seamlessly.
    engine.dispose()
    
    print_pool_status(engine, "After Dispose")


# ============================================================
# MAIN EXECUTION
# ============================================================
if __name__ == "__main__":
    demo_pool_lifecycle()
    demo_null_pool()
    demo_engine_dispose()
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,          # Maintain up to 5 steady-state connections
    max_overflow=10,      # Allow up to 10 additional temporary connections
    pool_timeout=30,      # Wait up to 30 seconds before throwing TimeoutError
    pool_recycle=1800,    # Recycle connections after 30 minutes (1800 seconds)
    pool_pre_ping=True,   # "Pre-ping" connection with 'SELECT 1' to ensure it's alive
)

metadata = MetaData()
employee = Table("employee", metadata, autoload_with=engine)


def print_pool_status(engine, label=""):
    """Utility to print current pool checkout metrics."""
    pool = engine.pool
    print(f"[{label}] Pool Status -> Size: {pool.size()} | Checked out: {pool.checkedout()} | Overflow: {pool.overflow()}")


# ============================================================
# 2. CHECKOUT & CHECKIN DEMONSTRATION
# ============================================================
def demo_pool_lifecycle():
    print("\n--- 1. Connection Checkout & Checkin ---")
    print_pool_status(engine, "Initial")

    # Checking out Connection 1
    with engine.connect() as conn1:
        print_pool_status(engine, "Conn 1 Checked Out")

        # Checking out Connection 2 concurrently
        with engine.connect() as conn2:
            print_pool_status(engine, "Conn 1 & 2 Checked Out")
            
            # Perform query on active connection
            res = conn2.execute(select(employee.c.name).limit(1)).scalar()
            print(f"Query Result: {res}")

    # Both connections returned to pool upon exiting context blocks
    print_pool_status(engine, "After Return to Pool")


# ============================================================
# 3. ADVANCED POOL CONFIGURATIONS
# ============================================================
def demo_null_pool():
    print("\n--- 2. NullPool (Disabling Pooling for Serverless/Short-lived Tasks) ---")
    
    # NullPool opens a fresh database connection every time and closes it immediately
    # Useful for AWS Lambda, serverless tasks, or when using external proxies like PgBouncer
    null_engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,
    )

    with null_engine.connect() as conn:
        result = conn.execute(text("SELECT pg_backend_pid()")).scalar()
        print(f"NullPool Execution Backend PID: {result}")
    
    null_engine.dispose()


# ============================================================
# 4. DISPOSING THE POOL
# ============================================================
def demo_engine_dispose():
    print("\n--- 3. Engine Disposal & Cleanup ---")
    print_pool_status(engine, "Before Dispose")

    # Closes all idle connections in the pool.
    # New checkouts will recreate connections seamlessly.
    engine.dispose()
    
    print_pool_status(engine, "After Dispose")


# ============================================================
# MAIN EXECUTION
# ============================================================
if __name__ == "__main__":
    demo_pool_lifecycle()
    demo_null_pool()
    demo_engine_dispose()