FROM tensorflow/tensorflow:nightly-jupyter as base
RUN apt-get update -y
RUN apt-get upgrade -y
RUN mkdir /work/
WORKDIR /work/
RUN pip install --upgrade pip
COPY ./ /work/
RUN pip install -r requirements.txt
RUN chmod -R 775 /work/
ENV FLASK_APP=app.py
RUN chmod +x /work/start.sh
CMD ["./start.sh"]