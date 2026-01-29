FROM nginx:alpine

# Remove default nginx site
RUN rm -rf /usr/share/nginx/html/*

# Copy static frontend files
COPY . /usr/share/nginx/html

EXPOSE 80
