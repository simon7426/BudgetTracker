FROM nginx:1.21.5-alpine

COPY dev.default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]