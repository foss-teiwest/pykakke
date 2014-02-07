from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, asynchronous
import time

filename = '../data/read.txt'


class MainHandler(RequestHandler):
    
    @asynchronous
    def get(self, pos_str='0'):
        self.file = open(filename)
        try:
            pos = int(pos_str)
        except ValueError:
            pos = 0
        self.pos = pos
        self._read()
        

    def _read(self):
        f = self.file
        f.seek(self.pos)
        text = f.read()
        self.pos = f.tell()
        if not text:
            IOLoop.instance().add_timeout(time.time() + 1, self._read)
        else:
            self.write({'pointer': self.pos, 'text': text})
            self.finish()
            f.close()
        
        

application = Application([
    (r"/(.*)", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888, '0.0.0.0')
    IOLoop.instance().start()