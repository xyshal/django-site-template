FROM nginx:1.21

# Standard configuration
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

# Certbot installation (untested)
RUN apt-get update && apt-get install -yf certbot python3-certbot-nginx
#RUN certbot --nginx

# Reload nginx automatically when the HTTPS cert renews
RUN echo "deploy-hook = nginx -s reload" >> /etc/letsencrypt/cli.ini
