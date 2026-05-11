FROM odoo:19.0

USER root

# Install additional system dependencies + boto3 for S3 storage
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages -r /tmp/requirements.txt

# Copy custom addons
COPY ./addons /mnt/extra-addons

# Copy Odoo config
COPY ./config/odoo.conf /etc/odoo/odoo.conf

USER odoo
