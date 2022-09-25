FROM nginx:latest
RUN apt-get update
ARG FILE
ENV PATH=/usr/share/nginx/html/index.html
ADD $FILE $PATH
ENTRYPOINT ["/usr/sbin/nginx", "-g"]
CMD ["daemon off;"]
