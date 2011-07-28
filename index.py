import web, os, cgi, time, sys, random, shutil
from stat import *
import convert

web.webapi.internalerror = web.debugerror
web.config.debug=False

# Upload/Download expire time
exp = 600 # 10 minutes

# Maximum file input size
cgi.maxlen = 50*1024*1024 # 50MB

# Directory to upload xls files to
upload_dir = 'xls_files/'

# Download directory
download_dir = 'xforms/'

# Director for templates
rootdir = os.path.abspath('templates') + '/'
template = web.template.render(rootdir)
        
urls = (
    '/', 'Index',
    '/(.*)', 'Index'
)
app = web.application(urls, globals(), autoreload=False)
main = app.wsgifunc()

class Index:        
    def GET(self, name=None):
        args = web.input()
        #If an error was raised, display it
        if 'e' in args:
            return template.index(error=args.e)
            
        #If an id is provided, then the conversion is complete
        elif 'id' in args:
            #If d is defined the user clicked the download link
            if 'd' in args:
                self.cleanup_files(download_dir)
                dname = download_dir+args.id
                files = os.listdir(dname)
                web.header('Content-Disposition', 'attachment; filename='+files[0])
                f = open(dname+'/'+files[0],'r')
                return f.read()
                
            #Otherwise just offer the link to download
            else:
                return template.index(id=args.id)
        
        #Else display the default page
        else:
            return template.index()
    
    #Uploading an xls file
    def POST(self):
        try:
            args = web.input(xlsfile={}) 
        except ValueError:
            return "File too large. Maximum file size is 50MB"
            
        if 'xlsfile' not in args:
            web.seeother('/')
        
        #Cleanup the file path  
        filepath = args.xlsfile.filename.replace('\\','/')
        filename = filepath.split('/')[-1]
        
        if not filename.lower().endswith('xls'):
            raise web.seeother('/?e=Only xls files are accepted')
        
        #Generate a unique folder to store the uploaded file in    
        ID = str(int(random.random()*1000000000000))
        os.mkdir(upload_dir+ID)  
        
        #Store the uploaded xls 
        fout = open(upload_dir+ID+'/'+filename,'w') 
        fout.write(args.xlsfile.file.read())
        fout.close()
        
        #Remove any expired uploads
        self.cleanup_files(upload_dir)
        
        #Convert the file. Report any errors, or offer the id of the
        #folder to download from
        try:
            download_ID = convert.convert(upload_dir +'/'+ID+'/'+filename)
        except:
            raise web.seeother('/?e='+ str(sys.exc_info()[1]))
        raise web.seeother('/?id=' + download_ID)
    
    #Iterate through the upload or download folder and remove any expired folders    
    def cleanup_files(self, dirty_dir):
        dirs = os.listdir(dirty_dir)
        for d in dirs:
            if os.path.isfile(dirty_dir+d):
                continue
        
            st=os.stat(dirty_dir + d)
            mtime = st[ST_MTIME]
            
            if time.time() - mtime > exp:
                shutil.rmtree(dirty_dir + d)


if __name__ == "__main__":
    app.run()

