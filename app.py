from flask import Flask, request, jsonify, render_template, abort
import psycopg2
import os

from logging import basicConfig, getLogger, DEBUG
basicConfig(level=DEBUG)
logger = getLogger(__name__)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
BASE = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET'])
def root():
    # 環境変数からサイトIDを取得
    site_id = os.environ['site_id']

    # 各情報を抽出
    site_detail = get_website_detail(site_id)
    blog_list = get_blog_list(site_id)
    product_list = get_product_list(site_id)
    navigation = get_navigation(site_id)

    html = render_template('root.html', site_detail=site_detail, blog_list=blog_list, product_list=product_list, navigation=navigation)
    return html

@app.route('/blog', methods=['GET'])
def blog_list():
    # 環境変数からサイトIDを取得
    site_id = os.environ['site_id']

    # 各情報を抽出
    site_detail = get_website_detail(site_id)
    blog_list = get_blog_list(site_id)
    navigation = get_navigation(site_id)

    html = render_template('blog_list.html', site_detail=site_detail, blog_list=blog_list, navigation=navigation)
    return html

@app.route('/blog/<custom_url>', methods=['GET'])
def blog_detail(custom_url):
    # 環境変数からサイトIDを取得
    site_id = os.environ['site_id']

    # 各情報を抽出
    site_detail = get_website_detail(site_id)
    blog_detail = get_blog_detail(site_id, custom_url)
    navigation = get_navigation(site_id)

    html = render_template('blog_detail.html', site_detail=site_detail, blog_detail=blog_detail, navigation=navigation)
    return html

@app.route('/products', methods=['GET'])
def products_list():
    # 環境変数からサイトIDを取得
    site_id = os.environ['site_id']

    # 各情報を抽出
    site_detail = get_website_detail(site_id)
    product_list = get_product_list(site_id)
    navigation = get_navigation(site_id)

    html = render_template('product_list.html', site_detail=site_detail, product_list=product_list, navigation=navigation)
    return html    

@app.route('/products/<custom_url>', methods=['GET'])
def product_detail(custom_url):
    # 環境変数からサイトIDを取得
    site_id = os.environ['site_id']

    # 各情報を抽出
    site_detail = get_website_detail(site_id)
    product_detail = get_product_detail(site_id, custom_url)
    navigation = get_navigation(site_id)

    html = render_template('blog_detail.html', site_detail=site_detail, product_detail=product_detail, navigation=navigation)
    return html

# global
def db_conn():
    # 環境変数からDBサーバの情報を取得
    pg_url = os.environ['pg_url']

    # connectionを生成
    conn = psycopg2.connect(pg_url)
    return conn

def get_website_detail(site_id):
    sql = 'SELECT domain_name, display_name, site_name, twitter_id, twitter_title, twitter_description, twitter_hashtag FROM cms2_website WHERE site_id=%s;'

    conn = db_conn()
    with conn.cursor() as cur:
        cur.execute(sql, (site_id,))
        result = cur.fetchone()

    site_info = {
        'domain_name': result[0],
        'display_name': result[1],
        'site_name': result[2],
        'twitter_id': result[3],
        'twitter_title': result[4],
        'twitter_description': result[5],
        'twitter_hashtag': result[6]
    }
    return site_info

def get_blog_list(site_id):
    sql = 'SELECT custom_url, title, tags, date FROM cms2_blog WHERE site_id=%s AND visible=True;'

    conn = db_conn()
    with conn.cursor() as cur:
        cur.execute(sql, (site_id,))
        results = cur.fetchall()

    blog_list = []
    for item in results:
        blog = {
            'custom_url': item[0],
            'title': item[1],
            'tags': item[2],
            'date': str(item[3])
        }
        blog_list.append(blog)
    return blog_list

def get_product_list(site_id):
    sql = 'SELECT product_code, product_name, photos FROM my_products WHERE site_id=%s ORDER BY release_date DESC;'

    conn = db_conn()
    with conn.cursor() as cur:
        cur.execute(sql, (site_id,))
        results = cur.fetchall()

    product_list = []
    for item in results:
        # 写真が複数だった場合の対応
        photos = item[2]
        if photos.count(',') > 0:
            tmp1 = photos.split(',')
        else:
            tmp1 = []
            tmp1.append(photos)

        product = {
            'product_code': item[0],
            'product_name': item[1],
            'photos': tmp1
        }
        product_list.append(product)
    return product_list

def get_blog_detail(site_id, custom_url):
    sql = 'SELECT title, summary, content_body, tags, date FROM cms2_blog WHERE site_id=%s AND custom_url=%s AND visible=True;'

    conn = db_conn()
    with conn.cursor() as cur:
        cur.execute(sql, (site_id, custom_url,))
        result = cur.fetchone()

    blog = {
        'title': result[0],
        'summary': result[1],
        'content_body': result[2],
        'tags': result[3],
        'date': str(result[4])
    }
    return blog

def get_product_detail(site_id, custom_url):
    sql = 'SELECT product_code, product_name, price, sammary, description, photos, release_date, keyword, sold_out, order_url FROM my_products WHERE site_id=%s AND custom_url=%s;'

    conn = db_conn()
    with conn.cursor() as cur:
        cur.execute(sql, (site_id, custom_url,))
        result = cur.fetchone()

    # 写真が複数だった場合の対応
    photos = result[5]
    if photos.count(',') > 0:
        tmp1 = photos.split(',')
    else:
        tmp1 = []
        tmp1.append(photos)

    if result[8] == True:
        sold_out = "True"
    else:
        sold_out = "False"

    product = {
        'product_code': result[0],
        'product_name': result[1],
        'price': str(result[2]),
        'sammary': result[3],
        'description': result[4],
        'photos': tmp1,
        'release_date': str(result[6]),
        'keyword': result[7],
        'sold_out': sold_out,
        'order_utl': result[9]
    }
    return product

def get_navigation(site_id):
    sql = 'SELECT url, name FROM cms2_navi WHERE site_id=%s ORDER BY priority ASC;'

    conn = db_conn()
    with conn.cursor() as cur:
        cur.execute(sql, (site_id,))
        results = cur.fetchall()

    navigation_list = []
    for item in results:
        navi = {
            'url': item[0],
            'name': item[1]
        }
        navigation_list.append(navi)
    return navigation_list


