FROM ubuntu:16.04

WORKDIR /dir
COPY script.sh .
RUN chmod +x script.sh
RUN apt-get update && apt-get install -y curl wget
CMD ["./script.sh"]
