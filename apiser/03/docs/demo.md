#### 蓝图
```bash

方案一:
html_bp.static('/statics', os.path.join(CONFIG.BASE_DIR, 'statics'))
html_bp静态文件注册路由: /html_bp/statics/
模版中static表示路径: template('rss.html', articles=data, static='/html/statics/rss_html')

方案二:
html_bp.static('/statics', os.path.join(CONFIG.BASE_DIR, './statics/rss_html'))
模版中static表示路径: template('rss.html', articles=data, static='/html/statics')


路由:/html/statics/css/main.css
文件:./statics/rss_html/css/main.css

# jinjia2 config: loader 必须使用相对路径
env = Environment(
    loader=PackageLoader('views.rss_json',  '../templates/rss_html'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']),
    enable_async=enable_async)
```
####
