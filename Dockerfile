FROM ubuntu:22.04
RUN echo "deb http://security.ubuntu.com/ubuntu focal-security main" | tee /etc/apt/sources.list.d/focal-security.list
RUN apt-get update && apt-get install -y python3 python3-pip imagemagick fonts-wqy-microhei libssl1.1
RUN pip install pysrt moviepy azure.cognitiveservices.speech
RUN apt-get -y install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools
RUN pip install fire

ADD policy.xml /etc/ImageMagick-6/policy.xml 

WORKDIR /data