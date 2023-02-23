#
FROM python:3.9

WORKDIR /home


ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update

RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-py39_23.1.0-1-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-py39_23.1.0-1-Linux-x86_64.sh -b \
    && rm -f Miniconda3-py39_23.1.0-1-Linux-x86_64.sh
#
COPY ./requirements.txt /home/requirements.txt

#RUN conda install --file /home/requirements.txt netCDF4 fastapi uvicorn pydantic

RUN conda config --add channels conda-forge
#RUN conda config --set channel_priority strict

RUN conda install -c conda-forge pip  -y
RUN conda install -c "conda-forge/label/cf202003" fastapi -y
RUN conda install --file /home/requirements.txt

RUN pip install -y Pydap
COPY ./app /home/app/

ENV PYTHONPATH "${PYTHONPATH}:/home/app/"


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
