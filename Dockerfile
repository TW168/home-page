FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
COPY index-traditional.html /usr/share/nginx/html/index-traditional.html
EXPOSE 80
