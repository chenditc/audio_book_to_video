FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip ImageMagick libssl1.1
RUN pip install pysrt moviepy 