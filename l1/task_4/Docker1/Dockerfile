FROM nginx:latest
RUN apt-get update
ENV PATH=/usr/share/nginx/html/index.html
ADD ./index.html $PATH
ENTRYPOINT ["/usr/sbin/nginx", "-g"]
CMD ["daemon off;"]
