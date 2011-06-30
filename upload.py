import web, cgi, time, os, sys
from stat import *
import convert
import index

# Maximum file input size
cgi.maxlen = 50*1024*1024 # 50MB

# Upload expire time
exp = 600 # 10 minutes

# Directory to upload xls files to
upload_dir = 'xls_files'

class Upload:
    def GET(self):
        raise web.seeother('/index')

    def POST(self):
        try:
            x = web.input(xlsfile={})
        except ValueError:
            return "File too large. Maximum file size is 50MB"
            
        if 'xlsfile' in x:
            filepath = x.xlsfile.filename.replace('\\','/')
            filename = filepath.split('/')[-1]
            
            if not filename.lower().endswith('xls'):
                raise web.seeother('/index/error/Only .xls files are accepted')
            
            fout = open(upload_dir +'/'+filename,'w') 
            fout.write(x.xlsfile.file.read())
            fout.close()
            self.cleanup_files()
            web.debug(upload_dir +'/'+filename)
            try:
                download_dir = convert.convert(upload_dir +'/'+filename)
            except:
                raise web.seeother('/index/error/'+ str(sys.exc_info()[1]))
        raise web.seeother('/index/' + download_dir)

    def cleanup_files(self):
        files = os.listdir(upload_dir)
        for f in files:
            st=os.stat(upload_dir + '/' + f)
            mtime = st[ST_MTIME]
            
            if time.time() - mtime > exp:
                os.remove(upload_dir + '/' + f)
                web.debug('Deleteing: ' + f)

    
