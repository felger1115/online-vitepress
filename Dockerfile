FROM node:24.4.0-bullseye-slim AS dep
WORKDIR /app
COPY view/ ./
RUN ls -al
RUN npm install

RUN npm run build

FROM python:3.11-slim-bullseye AS build
ARG dev

WORKDIR /app
COPY requirements.txt ./

RUN apt-get update && apt-get install -y tzdata vim
ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN if [[ ! -z "$dev" ]]; then \
        pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt; \
    else \
        pip install -r requirements.txt; \
    fi

FROM build AS prod
COPY . .
COPY --from=dep /app/node_modules /app/view/node_modules
COPY --from=dep /app/dist/spa/ /app/static

COPY --from=dep /usr/local/bin/node /usr/local/bin/
COPY --from=dep /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm && \
    ln -s /usr/local/lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx

EXPOSE 80
CMD ["hypercorn", "app:app", "--bind", "0.0.0.0:80", "--workers", "2", "--access-logfile", "-"]
