import os
from sanic import Sanic
app = Sanic(__name__)

# Serves files from the static folder to the URL /static

current_directory = os.path.dirname(os.path.abspath(__name__))
# static_directory = os.path.join(current_directory, 'client')

app.static('/static', current_directory)

# Serves the file /home/ubuntu/test.png when the URL /the_best.png
# is requested
# app.static('/the_best.png', '/est.png')

app.run(host="0.0.0.0", port=7000, debug=True)
