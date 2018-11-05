import subprocess

from flask import Flask
app = Flask(__name__)

@app.route('/')
def root_request():
 return "Health Check"

@app.route('/spider')
def run_spider():
  spider_name = "deloitte"
  subprocess.check_output(['scrapy', 'crawl', spider_name, "-o", "output.json"])
  with open ("output.json") as items_file:
    return items_file.read()


if __name__ == '__main__':
  app.run(port=5000)
