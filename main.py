#!/usr/bin/env python
import os
import jinja2
import webapp2
from Message import Message

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")
    
    def post(self):
        message_text = self.request.get("message")
        message = Message(text=message_text)
        message.put()
        return self.redirect_to("all")

class AllMessageHandler(BaseHandler):
    def get(self):
        #all_messages = Message.query(Message.text == "SmartNinja").fetch()
        all_messages = Message.query().fetch()
        params = { "messages": all_messages }
        return self.render_template("seznam_sporocil.html", params=params)

class MessageDetailHandler(BaseHandler):
    def get(self, sporocilo_id):
        message_model = Message.get_by_id(int(sporocilo_id))
        params = { "message": message_model }
        return self.render_template("sporocilo.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/seznam-sporocil', AllMessageHandler, "all"),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>', MessageDetailHandler)
], debug=True)
