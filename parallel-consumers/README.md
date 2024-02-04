The idea of this is to have the following:

- Docker compose for setting up all services.
- A producer container that will generate a big number of files, all with random alphanumeric content.
- Multiple consumer containers that will request files from the producer for processing.
- A monitoring container (Prometheus) that will be open for the consumer container to send metrics, which will be aggregated (and ideally visualized in real-time). Data should be available on a per-container. Using Grafana would be cool too.

## Installing on MacOS

https://docs.docker.com/compose/install/linux/#install-the-plugin-manually

```bash
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.24.2/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
```

(Last steps from https://github.com/docker/compose/issues/8630)

```bash
mkdir -p ~/.docker/cli-plugins
ln -sfn /opt/homebrew/opt/docker-compose/bin/docker-compose ~/.docker/cli-plugins/docker-compose
```

```bash
docker compose version
```
