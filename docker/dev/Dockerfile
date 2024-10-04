FROM amd64/python:3.10-buster
RUN apt update && apt install -y ffmpeg
RUN python -m pip install torch==2.4.1+cpu --extra-index-url https://download.pytorch.org/whl/cpu
RUN mkdir -p /tgcalls-gate/
WORKDIR /tgcalls-gate/
COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt
RUN pip install -r requirements-dev.txt