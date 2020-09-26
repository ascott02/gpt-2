import web
import re
import config
import base64

import fire
import json
import os
import numpy as np
import tensorflow as tf
import sys
sys.path.append("../src/")

import model, sample, encoder

from urllib.parse import urlparse,quote,unquote

# web.py
urls = (
    '/', 'index',
    '/index', 'index',
    '/login', 'login',
    '/songs', 'songs',
    '/about', 'about',
)
render = web.template.render('templates/', base='layout')
app = web.application(urls, globals(), autoreload=False)

model_name = "run1"
enc = encoder.get_encoder(model_name)
hparams = model.default_hparams()
with open(os.path.join('../models', model_name, 'hparams.json')) as f:
    hparams.override_from_dict(json.load(f))

temperature = 1.618
batch_size = 1
length = 100
top_p = 40
top_k = 10
seed = 42







def generate_song(length=1000, nsamples=1, batch_size=1, seed=42, top_k=0, top_p=40, temperature=1.618, start_text="hello"):
    if length is None:
        length = hparams.n_ctx
    elif length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

    with tf.Session(graph=tf.Graph()) as sess:
        context = tf.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)


        output = sample.sample_sequence(
            hparams=hparams, length=length,
            # start_token=enc.encoder['<|endoftext|>'],
            context=context,
            batch_size=batch_size,
            temperature=temperature, top_k=top_k, top_p=top_p
        )[:, 1:]

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join('../models', model_name))
        saver.restore(sess, ckpt)


        generated = 0
        text_output = start_text
        context_tokens = enc.encode(start_text)
        while nsamples == 0 or generated < nsamples:
            # out = sess.run(output)

            out = sess.run(output, feed_dict={
                context: [context_tokens for _ in range(batch_size)]
            })[:, len(context_tokens):]

            for i in range(batch_size):
                generated += batch_size
                text = enc.decode(out[i])
                # print("=" * 40 + " SAMPLE " + str(generated) + " " + "=" * 40)
                # print(text)
                text_output += text
    return (text_output)

class index:

    def GET(self, *args):

        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            page = """"""
            return render.index(page)
        else:
            raise web.seeother('/login')

    def POST(self, *args):
        x = web.input()
        start_text = str(x['start_text'])
        # start_text = start_text.lower()
        seed = int(x['seed_input'])
        temp = float(x['temperature_input'])
        top_p = float(x['top_p_input'])
        length = int(x['length_input'])
        web.debug(start_text)

        sample_output = generate_song(start_text=start_text, temperature=temp, top_p=top_p, length=length, seed=seed)
        web.debug(sample_output)

        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:

            return render.index(sample_output)
        else:
            raise web.seeother('/login')

class songs:

    def GET(self, *args):
        x = web.input()
        songs_file = "../planet_booty_songs.json"
        with open(songs_file, "r") as f:
            songs = json.load(f)
        page = "<form action='/songs'>"
        page += "<select name='song' id='song' onchange='this.form.submit()'>"
        for song in songs['songs']:
            # page += "<a href=/songs?song=" + quote(song['name']) + ">" + song['name'].replace(u"\u2018", "'").replace(u"\u2019", "'").strip().lstrip() + "</a><br>"
            page += "<option value='" + quote(song['name']) + "'>" + song['name'].replace(u"\u2018", "'").replace(u"\u2019", "'").strip().lstrip() + "</option>"
        page += "</select>"
        page += "</form>"
        # page += """<table width="60%"><tr><td width="20%" align="left" valign="top">"""

        # page += """</td><td width="60%" align="left" valign="top">"""
        # web.debug(songs)

        try:
            ssong = unquote(x['song'])
            web.debug(ssong)
            for tsong in songs['songs']:
                if ssong == tsong['name']:
                    for line in tsong['lyrics'].split("\n"):
                        page += line + "<br>"
        except:
            page += ""

        # page += """</td></tr></table>"""



        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            return render.songs(page)
        else:
            raise web.seeother('/login')

class about:

    def GET(self, *args):
        page = """"""
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            return render.about(page)
        else:
            raise web.seeother('/login')

class login:

    def GET(self):
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        authreq = False
        if auth is None:
            authreq = True
        else:
            auth = re.sub('^Basic ','',auth)
            username,password = base64.b64decode(auth).decode().split(':')
            if (username,password) in config.allowed:
                raise web.seeother('/')
            else:
                authreq = True
        if authreq:
            web.header('WWW-Authenticate','Basic realm="Auth example"')
            web.ctx.status = '401 Unauthorized'
            return


if __name__ == "__main__":



    app.run()

