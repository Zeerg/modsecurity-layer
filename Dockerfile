FROM lambci/lambda:build-python3.7

ENV LIBMODSEC_VERSION=3.0.3
ENV PYMODSEC_VERSION=0.0.4

RUN mkdir -p /tmp/modsecbuild
WORKDIR /tmp/modsecbuild

# Build Modsecurity
RUN curl -L -o "modsec.tar.gz" "https://github.com/SpiderLabs/ModSecurity/releases/download/v${LIBMODSEC_VERSION}/modsecurity-v${LIBMODSEC_VERSION}.tar.gz" && \
    tar xf modsec.tar.gz && \
    cd modsecurity-v${LIBMODSEC_VERSION} && \
    ./build.sh && \
    ./configure --prefix=/opt/ && \
    make -j 8 && \
    make install && \
    ldconfig


# Build Pymodsecurity
WORKDIR /opt/python
RUN pip install pybind11

RUN pip install --target=/opt/python/ \
    --global-option=build_ext --global-option="-L/var/lang/lib:/opt/lib" \
    --global-option=build_ext --global-option="-I/var/lang/include/python3.7m:/opt/include" \
    pymodsecurity==${PYMODSEC_VERSION}

WORKDIR /opt

# Workaround for lambda not finding the library
RUN rm -rf lib/libmodsecurity.so && \
    rm -rf lib/libmodsecurity.so.3 && \
    mv lib/libmodsecurity.so.${LIBMODSEC_VERSION} lib/libmodsecurity.so.3

# Basic rules and fixing unicode mapping error
COPY basic_rules.conf /opt/lib/
COPY unicode.mapping /opt/lib/

# Switch our workdir back to task
WORKDIR /var/task