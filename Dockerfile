# Use the existing image as a base
FROM theosotr/sqlite3-test

# Install Python and pip
RUN sudo apt-get update && \
    sudo apt-get install -y python3 python3-pip && \
    sudo apt-get clean

# Optionally set Python3 as the default
RUN sudo ln -s /usr/bin/python3 /usr/bin/python

# Set working directory if you want
WORKDIR /workspace

# Default shell
CMD ["/bin/bash"]
