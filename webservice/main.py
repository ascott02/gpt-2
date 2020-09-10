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

# web.py
urls = (
    '/', 'index',
    '/login', 'login',
)

model_name = "run1"
enc = encoder.get_encoder(model_name)
hparams = model.default_hparams()
with open(os.path.join('../models', model_name, 'hparams.json')) as f:
    hparams.override_from_dict(json.load(f))

def generate_song(length=1000, nsamples=1, batch_size=1, seed=42, top_k=0, top_p=40, temperature=1.618):
    if length is None:
        length = hparams.n_ctx
    elif length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

    with tf.Session(graph=tf.Graph()) as sess:
        np.random.seed(seed)
        tf.set_random_seed(seed)

        output = sample.sample_sequence(
            hparams=hparams, length=length,
            start_token=enc.encoder['<|endoftext|>'],
            batch_size=batch_size,
            temperature=temperature, top_k=top_k, top_p=top_p
        )[:, 1:]

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join('../models', model_name))
        saver.restore(sess, ckpt)

        generated = 0
        text_output = ""
        while nsamples == 0 or generated < nsamples:
            out = sess.run(output)
            for i in range(batch_size):
                generated += batch_size
                text = enc.decode(out[i])
                # print("=" * 40 + " SAMPLE " + str(generated) + " " + "=" * 40)
                # print(text)
                text_output += text

    return (text)

class index:

    def GET(self, *args):

# start text: <input type="input" name="start_text" value="I want to" /><br/>
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            return """ <html><head></head><body>
<h1>Planet Booty Generator</h1>
<form method="POST" action="">
temperature: <input type="input" name="temperature" value="1.618" /><br/>
top_p: <input type="input" name="top_p" value="40" /><br/>
length: <input type="input" name="length" value="1000" /><br/>
<input type="submit" />
</form>
</body></html> """
        else:
            raise web.seeother('/login')

    def POST(self, *args):
        x = web.input()
        # start = str(x['start_text'])
        temp = float(x['temperature'])
        top_p = float(x['top_p'])
        length = int(x['length'])

        sample_output = generate_song(temperature=temp, top_p=top_p, length=length)

        page = """ <html><head></head><body>
<h1>Planet Booty Generator</h1>
<form method="POST" action="">
temperature: <input type="input" name="temperature" value=""" + str(temp) + """ /><br/>
top_p: <input type="input" name="top_p" value=""" + str(top_p) + """ /><br/>
length: <input type="input" name="length" value=""" + str(length) + """ /><br/>
<input type="submit" />
<pre>""" + sample_output + """</pre>
</form>
</body></html> """

        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            return page
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

app = web.application(urls, globals(), autoreload=False)

if __name__ == "__main__":
    app.run()

