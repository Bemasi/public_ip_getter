FROM ubuntu:22.04

RUN apt update && apt install -y wget gnupg2 ca-certificates && \
    wget -qO - https://proton.me/download/bridge/proton-bridge.asc | gpg --dearmor -o /usr/share/keyrings/proton-bridge.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/proton-bridge.gpg] https://proton.me/download/bridge/linux stable main" > /etc/apt/sources.list.d/proton-bridge.list && \
    apt update && apt install -y protonmail-bridge

CMD ["protonmail-bridge", "--noninteractive"]