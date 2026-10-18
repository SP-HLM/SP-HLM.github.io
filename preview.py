"""Local static preview with byte-range video seeking. python3 preview.py"""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os,re
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(Path(__file__).parent),**kwargs)
 def send_head(self):
  path=self.translate_path(self.path)
  value=self.headers.get('Range','')
  if not value or not os.path.isfile(path):return super().send_head()
  size=os.path.getsize(path);m=re.fullmatch(r'bytes=(\d*)-(\d*)',value)
  if not m or not size:
   self.send_error(416);return None
  start=int(m[1]) if m[1] else max(0,size-int(m[2] or 0))
  end=min(int(m[2]),size-1) if m[1] and m[2] else size-1
  if start>=size or end<start:
   self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.end_headers();return None
  f=open(path,'rb');f.seek(start);self.remaining=end-start+1
  self.send_response(206);self.send_header('Content-Type',self.guess_type(path));self.send_header('Accept-Ranges','bytes');self.send_header('Content-Range',f'bytes {start}-{end}/{size}');self.send_header('Content-Length',str(self.remaining));self.end_headers();return f
 def copyfile(self,source,outputfile):
  try:
   if not hasattr(self,'remaining'):return super().copyfile(source,outputfile)
   while self.remaining:
    data=source.read(min(self.remaining,262144))
    if not data:break
    outputfile.write(data);self.remaining-=len(data)
  except (BrokenPipeError,ConnectionResetError):pass
  finally:
   if hasattr(self,'remaining'):del self.remaining
if __name__=='__main__':
 print('Local: http://localhost:8765',flush=True)
 ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
