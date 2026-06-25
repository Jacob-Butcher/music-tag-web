FROM python:3.9-slim

LABEL title="Music Tag Web | 音乐标签网页版"
LABEL description="『音乐标签』Web版是一款可以编辑歌曲的标题，专辑，艺术家，歌词，封面等信息的应用程序"
LABEL authors="xhongc"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY ./requirements .
RUN pip install --no-cache-dir -r base.txt

COPY ./compose/local/django/start /start
RUN chmod +x /start

COPY . .

CMD ["/start"]
