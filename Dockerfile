FROM tensorflow/tensorflow:latest

ENV PORT=8081
ENV IP=127.0.0.1
ENV PROTO=http
ENV MODEL=distilbert

COPY requirements.txt /
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
# Copy predictor script and ML model
COPY urlpredictor.py /
COPY distilbert /distilbert

EXPOSE ${PORT}

# Create a script that runs the model server so we can use environment variables
# while also passing in arguments from the docker command line
RUN echo '#!/bin/bash \n\n\
python3 urlpredictor.py --port=${PORT} --ip=${IP} --proto=${PROTO} --model=${MODEL} \
"$@"' > /usr/bin/predictor_serving_entrypoint.sh \
&& chmod +x /usr/bin/predictor_serving_entrypoint.sh

ENTRYPOINT ["/usr/bin/predictor_serving_entrypoint.sh"]