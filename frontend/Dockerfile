FROM nginx:1.20.1

# Add nodejs
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  apt-utils nodejs && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npx ng build --prod 

RUN cp -R dist/qrisq-onbrdng-webspa/* /usr/share/nginx/html

ENTRYPOINT ["nginx", "-g", "daemon off;"]