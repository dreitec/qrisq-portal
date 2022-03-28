FROM nginx:1.20.1

# Add nodejs
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  apt-utils nodejs python3-pip && \
  rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install awscli

WORKDIR /opt/app

COPY . .

RUN npm install

RUN npx ng build --prod

RUN cp -R dist/qrisq-onbrdng-webspa/* /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY start.sh /opt/app/start.sh

CMD ["sh", "/opt/app/start.sh"]
