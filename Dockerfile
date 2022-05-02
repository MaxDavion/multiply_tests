FROM mcr.microsoft.com/playwright/python

WORKDIR /app
ADD . /app

# Install allure-cli
RUN apt-get update
RUN apt-get install default-jre -y
RUN apt-get install default-jdk -y

RUN curl -o allure-2.13.8.tgz -OLs https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.8/allure-commandline-2.13.8.tgz
RUN tar -zxvf allure-2.13.8.tgz -C /opt/
RUN ln -s /opt/allure-2.13.8/bin/allure /usr/bin/allure
RUN rm -f allure-2.13.8.tgz

# Install any needed packages specified in requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
