# Use the existing image as a base
FROM theosotr/sqlite3-test

# Install Python and pip
RUN sudo apt-get update && \
    sudo apt-get install -y python3 python3-pip && \
    sudo apt-get clean

# Optionally set Python3 as the default
RUN sudo ln -s /usr/bin/python3 /usr/bin/python

RUN cd ~ && \
    sudo apt install -y wget tar && \
    wget https://www.sqlite.org/2025/sqlite-autoconf-3490200.tar.gz && \
    tar zxvf sqlite-autoconf-3490200.tar.gz && \
    cd sqlite-autoconf-3490200 && \
    sudo ./configure && \
    sudo make && \
    sudo mv sqlite3 /usr/bin/sqlite3-3.49.2

# Set working directory if you want
WORKDIR /workspace

# Default shell
CMD ["/bin/bash"]
