import web, os
import upload
import download


# Download expire time
exp = 3600 # 1 hour

rootdir = os.path.abspath(os.path.dirname('templates/')) + '/'
render = web.template.render(rootdir)
        
urls = (
    '/upload', 'upload.Upload',
    '/index', 'Index',
    '/index/(.*)', 'Index',
    '/xform/(.*)', 'download.Download'
)
app = web.application(urls, globals())

class Index:        
    def GET(self, name=None):
        return render.index(name)
        
    def cleanup_files(self):
        files = os.listdir(download_dir)
        for f in files:
            web.debug("Investigating: " + download_dir + f)
            st=os.stat(download_dir + f)
            mtime = st[ST_MTIME]
            
            if time.time() - mtime > exp:
                for root, dirs, nested_files in os.walk(download_dir+f, topdown=False):
                    for name in nested_files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(download_dir+f)
                web.debug('Deleteing: ' + download_dir + f)

if __name__ == "__main__":
    app.run()

