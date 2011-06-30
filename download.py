import web, os       
        
class Download:
    def GET(self, path):
        fname = path.split('/')[-1]
        web.header('Content-Disposition', 'attachment; filename='+fname)
        f = open(path,'r')
        return f.read()
        
    
