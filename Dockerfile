FROM python:3.10-buster


ENV WORKDIR_PATH /home/ec2-user/showmeplace-api

ENV USER_CONTAINER 1919
ENV DOCKER 1

RUN mkdir -p $WORKDIR_PATH
WORKDIR $WORKDIR_PATH
RUN pip install "uvicorn[standard]"
RUN apt-get update -y && apt-get install vim nano -y && pip install -U pipenv

COPY --chmod=0444 ./Pipfile* ./
RUN pipenv install --deploy --system --clear

COPY --chmod=0444 . .
RUN find $WORKDIR_PATH -type d -exec chown $USER_CONTAINER:$USER_CONTAINER {} \;
RUN find $WORKDIR_PATH -type d -exec chmod 755 {} \;

USER $USER_CONTAINER
#CMD python main.py
CMD uvicorn main:app --host 0.0.0.0 --port 8000