from sanic import Sanic
from sanic.response import json, html, text
from sanic.exceptions import NotFound
from feedparser import parse
from jinja2 import Template

app = Sanic()
app.static('/static', './')

# 后面会使用更方便的模板引用方式
template = Template(
    """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>rss阅读</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
<article class="markdown-body">
    {% for article in articles %}
    <b><a href="{{article.link}}">{{article.title}}</a></b><br/>
    <i>{{article.published}}</i><br/>
    <hr/>
    {% endfor %}
</article>
</body>
</html>
    """
)

@app.exception(NotFound)
def ignore_404s(request, exception):
    return text("Yep, I totally found the page: {}--{}".format(request.url, exception),
                status=404)

@app.route("/")
async def index(request):
    url = 'http://blog.howie6879.cn/atom.xml'
    feed = parse(url)
    articles = feed['entries']
    data = []
    for article in articles:
        data.append({"title": article["title_detail"]["value"], "link": article["link"]})
    return json(data)


@app.route("/html")
async def rss_html(request):
    url = "http://blog.howie6879.cn/atom.xml"
    feed = parse(url)
    articles = feed['entries']
    data = []
    for article in articles:
        data.append(
            {"title": article["title_detail"]["value"], "link": article["link"], "published": article["published"]})
    html_content = template.render(articles=data)
    return html(html_content)

if __name__ == '__main__':
    app.run()
