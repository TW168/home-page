FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html
COPY index-traditional.html /usr/share/nginx/html/index-traditional.html
COPY aitherios.mp3 /usr/share/nginx/html/aitherios.mp3
EXPOSE 80
