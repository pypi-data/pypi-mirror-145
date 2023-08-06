FROM python:3
MAINTAINER Christian Witzler <c.witzler@fz-juelich.de>

# pipeline tools
RUN pip3 install --no-cache-dir prospector bandit mypy pytest anybadge coverage
RUN git clone https://github.com/wbazant/argdown.git && python3 argdown/setup.py build

# projekt dependencies
RUN apt-get update && apt-get install -y libopenmpi-dev && apt-get clean
RUN pip3 install --no-cache-dir flask mpi4py python_papi pynvml
RUN pip3 install --no-cache-dir psutil
RUN pip3 install --no-cache-dir flask-login

