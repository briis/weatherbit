FROM ghcr.io/ludeeus/devcontainer/integration:stable

RUN apt update \
    && sudo apt install -y libpcap-dev vim curl jq \
    && mkdir -p /opt \
    && cd /opt \
    && git clone --depth=1 -b dev https://github.com/home-assistant/core.git hass \
    && python3 -m pip --disable-pip-version-check install --upgrade ./hass \
    && python3 -m pip install flake8 \
    && ln -s /workspaces/weatherbit/custom_components/weatherflow /opt/hass/homeassistant/components/weatherbit
