#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL at $HOST:$PORT..."
until python3 -c "
import psycopg2, os, sys
try:
    psycopg2.connect(host=os.environ['HOST'], port=os.environ.get('PORT','5432'), user=os.environ['USER'], password=os.environ['PASSWORD'], dbname='postgres')
    sys.exit(0)
except: sys.exit(1)
" 2>/dev/null; do
  sleep 2
done
echo "PostgreSQL is ready."

# Check if Odoo DB is initialized
python3 -c "
import psycopg2, os, sys
try:
    conn = psycopg2.connect(host=os.environ['HOST'], port=os.environ.get('PORT','5432'), user=os.environ['USER'], password=os.environ['PASSWORD'], dbname='arlet_odoo')
    cur = conn.cursor()
    cur.execute(\"SELECT to_regclass('public.ir_module_module')\")
    result = cur.fetchone()[0]
    conn.close()
    sys.exit(0 if result else 1)
except: sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "Database not initialized. Running odoo -i base..."
    odoo --config=/etc/odoo/odoo.conf -i base --stop-after-init --no-http
    echo "Database initialization complete."
fi

echo "Starting Odoo..."
exec odoo --config=/etc/odoo/odoo.conf
