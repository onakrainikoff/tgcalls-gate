FROM amd64/python:3.10-buster
RUN apt update && apt install -y ffmpeg
RUN python -m pip install torch==2.4.1+cpu --extra-index-url https://download.pytorch.org/whl/cpu
RUN mkdir -p /tgcalls-gate/
RUN mkdir -p /tgcalls-gate/scripts/
RUN mkdir -p /tgcalls-gate/data/
WORKDIR /tgcalls-gate/
COPY src scripts
COPY default.config.yaml default.config.yaml
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD python scripts/main.py
