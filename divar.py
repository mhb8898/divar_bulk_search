import requests
from fake_useragent import UserAgent
from multiprocessing.pool import ThreadPool
import requests
from bs4 import BeautifulSoup
import flask
from flask import Response, stream_with_context
from urllib.parse import unquote

urls = ['tehran', 'mashhad', 'karaj', 'shiraz', 'isfahan', 'ahvaz', 'tabriz', 'kermanshah', 'qom', 'rasht', 'abadan', 'abadeh', 'abdanan', 'abyek', 'azarshahr', 'astara', 'astaneh-ashrafiyeh', 'ashkhaneh', 'aq-qala', 'amol', 'abhar', 'arak', 'ardabil', 'ardakan', 'urmia', 'azna', 'asadabad', 'esfar%C4%81yen', 'eslamabad-gharb', 'eslamshahr', 'oshnavieh', 'isfahan', 'alvand', 'aligudarz', 'andimeshk', 'ahar', 'ahvaz', 'izeh', 'iranshahr', 'ilam', 'eyvan', 'babol', 'babolsar', 'baneh', 'bojnurd', 'borazjan', 'borujerd', 'boroujen', 'bam', 'bonab', 'bandar-imam-khomeini', 'bandar-anzali', 'bandar-torkaman', 'bandar-abbas', 'bandar-kangan', 'bandar-ganaveh', 'bandar-mahshahr', 'bushehr', 'bukan', 'behbahan', 'behshahr', 'bijar', 'birjand', 'parsabad', 'piranshahr', 'pishva', 'takestan', 'talesh', 'tabriz', 'torbat-jam', 'tonekabon', 'tuyserkan', 'tehran', 'javanrud', 'juybar', 'jahrom', 'jiroft', 'chaboksar', 'chabahar', 'chalus', 'chahar-dangeh', 'hamidia', 'khorramabad', 'khorramdarreh', 'khorramshahr', 'khalkhal', 'khomein', 'khoy', 'darab', 'damghan', 'dezful', 'damavand', 'dorud', 'dogonbadan',
        'dehdasht', 'dehloran', 'ramsar', 'ramhormoz', 'rasht', 'rafsanjan', 'rudsar', 'zabol', 'zahedan', 'zarand', 'zanjan', 'sari', 'saveh', 'sabzevar', 'sarab', 'saravan', 'sarpol-zahab', 'sardasht', 'saqqez', 'salmas', 'semnan', 'sonqor', 'sanandaj', 'susangerd', 'sahand', 'siahkal', 'sirjan', 'shahroud', 'shahin-dej', 'shush', 'shooshtar', 'sadra', 'shahrekord', 'shiraz', 'shirvan', 'someh-sara', 'taleqan', 'tabas', 'aliabad-katul', 'farrokhshahr', 'ferdows', 'fereydunkenar', 'falavarjan', 'fuman', 'qaemshahr', 'ghayen', 'qorveh', 'qazvin', 'qeshm', 'qom', 'qeydar', 'kashan', 'karaj', 'kordkuy', 'kerman', 'kermanshah', 'kelachay', 'kangavar', 'kuhdasht', 'kish', 'gorgan', 'garmsar', 'golpayegan', 'gomishan', 'gonabad', 'gonbad-kavus', 'lahijan', 'lordegan', 'langarud', 'masal', 'maku', 'mahalat', 'mohammadiyeh', 'mahmudabad', 'maragheh', 'marand', 'marivan', 'masjed-soleyman', 'meshgin-shahr', 'mashhad', 'malayer', 'mahabad', 'miandoab', 'mianeh', 'meybod', 'minab', 'najafabad', 'nasimshahr', 'nazarabad', 'naqadeh', 'neka', 'nur', 'nurabad', 'nowshahr', 'nahavand', 'neyshabur', 'hamedan', 'yasuj', 'yazd']

ua = UserAgent()


def get(city, word):
    url = "http://divar.ir/s/{}".format(city, word)
    headers = {
        'User-Agent': ua.random,
    }
    doc = requests.get(url, headers=headers, params=[("q", word), ])
    city = unquote(city)
    if doc.status_code == 200:
        html_doc = doc.text
        soup = BeautifulSoup(html_doc, 'html.parser')
    else:
        return city, "error {}".format(doc.status_code)

    return "<a href={}>{}</a>".format(doc.url,city), str(len(soup.find_all(class_="post-card")))


app = flask.Flask(__name__)


@app.route("/<word>")
def main(word):
    def response():
        yield "<pre>"
        pool = ThreadPool(processes=10)
        async_result = [pool.apply_async(get, (city, word)) for city in urls]
        for res in async_result:
            yield " ".join(res.get())+"\n"

    return Response(stream_with_context(response()), mimetype="text/html")
