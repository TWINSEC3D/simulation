# Base stage for common dependencies
FROM ubuntu AS base

WORKDIR /app

# Install required packages
RUN apt-get update && apt-get install -y \
    systemd procps nano curl gnupg apt-transport-https gnupg2 inotify-tools python3-docker python3-setuptools python3-pip gcc python3-dev musl-dev libpq-dev python3-tk git postgresql-client

RUN curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | gpg --no-default-keyring --keyring gnupg-ring:/usr/share/keyrings/wazuh.gpg --import && chmod 644 /usr/share/keyrings/wazuh.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main" | tee -a /etc/apt/sources.list.d/wazuh.list
RUN curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | apt-key add -
RUN apt-get update
RUN echo "deb https://packages.wazuh.com/4.x/apt/ stable main" > /etc/apt/sources.list.d/wazuh.list
RUN WAZUH_MANAGER="wazuh.manager" apt-get install -y wazuh-agent=4.7.2-1
RUN update-rc.d wazuh-agent defaults 95 10
RUN service wazuh-agent start

# Copy all scripts
COPY scripts /scripts

# Give permissions
RUN chmod +x /scripts/wait-for-init.sh

# Install Python packages
RUN pip3 install psycopg2-binary --break-system-packages sqlalchemy

# Setup Sun-Valley-ttk-theme for HMI
RUN git clone https://github.com/rdbende/Sun-Valley-ttk-theme.git && \
    cd Sun-Valley-ttk-theme && python3 setup.py install
