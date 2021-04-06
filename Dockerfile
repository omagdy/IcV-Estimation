FROM python:latest

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install dcm2niix -y
RUN mkdir -p /app/nifti_converted_output

RUN mkdir -p /app/brain_extraction
RUN apt-get install cmake -y
WORKDIR /ants
RUN git clone https://github.com/ANTsX/ANTs.git
RUN mkdir build install
WORKDIR build
RUN cmake -DUSE_VTK=OFF \
     -DBUILD_TESTING=OFF \
     -DRUN_LONG_TESTS=OFF \
     -DRUN_SHORT_TESTS=OFF \
    -DBUILD_SHARED_LIBS=OFF \
    ../ANTs 2>&1 | tee cmake.log
RUN make -j 4 2>&1 | tee build.log
WORKDIR ANTS-build
RUN make install 2>&1 | tee install.log
ENV ANTSPATH="/opt/ANTs/bin/"
ENV PATH="${ANTSPATH}:$PATH"
RUN which antsBrainExtraction.sh

WORKDIR /app/icv
COPY . .

RUN mkdir -p /app/output
