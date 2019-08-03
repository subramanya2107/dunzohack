# build environment
FROM node:10.15.1-alpine as clientbuild
WORKDIR /client
COPY ./client/package.json /client/package.json
RUN npm install --silent
COPY ./client /client
RUN npm run build

FROM node:10.15.1-alpine

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install
# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source
COPY . .
COPY --from=clientbuild /client/build/. /usr/src/app/public/.
EXPOSE 3000
CMD [ "npm", "start" ]