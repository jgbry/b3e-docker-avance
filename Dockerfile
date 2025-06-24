FROM jellyfin/jellyfin:latest
CMD ["jellyfin"]

#docker build -t jellyfin-custom .
#docker run -d --name jellyfin -p 8096:8096 -v jellyfin-config:/config jellyfin-custom