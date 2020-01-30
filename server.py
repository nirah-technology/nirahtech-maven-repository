import json
import urllib2
import ssl
import os
import sys
import re
import shutil
import time
import platform
from threading import Thread
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# from http.server import BaseHTTPRequestHandler, HTTPServe

is_currently_updating = False

class LocalMavenRepositoryUpdater(Thread):
    def __init__(self):
        Thread.__init__(self)

    def initialize_context(self):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

    def extract_artifact_id_and_version(self, jar_file):
        jar_file = jar_file.replace(".jar", '')
        informations = jar_file.split('-')
        try:
            VERSION = re.search(r'([0-9]){1,}([.]([0-9]){1,}){0,}.+',jar_file).group(0)
            ARTIFACT_ID = jar_file.replace("-"+VERSION, '')
            return {"artifact": ARTIFACT_ID, "version": VERSION}
        except:
            print(jar_file)
            return None

    def execute_maven_build_command(self, path_where_move = None):
        default_path = os.getcwd()
        if (path_where_move != None):
            os.chdir(str(path_where_move))
        maven_command = "mvn clean install"
        os.system(maven_command)
        if (path_where_move != None):
            os.chdir(default_path)

    def copy_local_for_remote(self, project):
        nirah_mavn_repo_git_project = str(os.getcwd()+'/').replace("\\", "/").replace("//", "/").replace("//", "/")
        for root, directory_name, file_name in os.walk(nirah_mavn_repo_git_project):
            for file in file_name:
                if ("maven-metadata-local.xml" in str(file)):
                    path = str(os.getcwd()+"/repository/io/nirahtech/"+project["artifact"]+'/'+str(file)).replace("\\", "/").replace("//", "/").replace("//", "/")
                    shutil.copyfile(path, path.replace("-local", ''))
        nirah_mavn_repo_git_project += '/repository/io/nirahtech/'+project["artifact"]+'/'+project["version"]+'/'
        for root, directory_name, file_name in os.walk(nirah_mavn_repo_git_project):
            for file in file_name:
                if ("maven-metadata-local.xml" in str(file)):
                    path = str(nirah_mavn_repo_git_project+str(file)).replace("\\", "/").replace("//", "/").replace("//", "/")
                    shutil.copyfile(path, path.replace("-local", ''))

    def delete_directory(self, directory, is_root=True):
        if (not is_root):
            if (platform.system() == 'Windows'):
                os.system("del /F /S /Q /A "+directory+".git")
                os.system("rmdir .git")
            else:
                os.system("rm -rf "+directory+".git")
        shutil.rmtree(directory, ignore_errors=False, onerror=None)

    def execute_maven_install_command(self, url, data):
        maven_command = "mvn install:install-file -DgroupId=io.nirahtech -DartifactId="+data["artifact"]+" -Dversion="+data["version"]+" -Dfile="+url+" -Dpackaging=jar -DgeneratePom=true -DlocalRepositoryPath=./repository/ -Durl="+str(os.getcwd())+"/repository/ -DcreateChecksum=true"
        os.system(maven_command)

    def update(self):
        http_response_data = [None]
        context = self.initialize_context()

        per_page = 1
        page = 1
        private_token = "mQ-WxRsF8djwo1upt1yH"
        server = "gitlab.nirah-technology.fr"
        api = "api/v4/projects"
        nirahtech_projects = "nirahtech-projects"
        git_projects = "git-projects"
        base_url = str("https://"+server)

        while (len(http_response_data) != 0):
            url = str(base_url + '/' + api + "?private_token="+private_token+"&per_page=" + str(per_page) + "&page=" + str(page))
            response = urllib2.urlopen(url, context=context)
            http_response_data = json.loads(str(response.read()))
            page += 1

            if (len(http_response_data) > 0):
                project_name = str(http_response_data[0]["name"]) 
                project_url = str(http_response_data[0]["http_url_to_repo"])
                if (str('/'+nirahtech_projects+'/') in project_url):
                    os.system("git clone " + project_url + " ./"+ git_projects +'/'+project_name)

                    downloaded_project_path = str("./"+ git_projects +'/'+project_name)
                    self.execute_maven_build_command(downloaded_project_path)
                    target = "target"

                    builded_project_path = downloaded_project_path + '/' + target
                    if (os.path.exists(builded_project_path) and os.path.isdir(builded_project_path)):
                        for potential_jar_file in os.listdir(builded_project_path):
                            if (str(potential_jar_file).endswith(".jar")):
                                target_and_jar_path = str(builded_project_path + '/' + str(potential_jar_file))
                                data = self.extract_artifact_id_and_version(potential_jar_file)
                                if (data != None):
                                    self.execute_maven_install_command(target_and_jar_path, data)
                                    self.copy_local_for_remote(data)
                    try:
                        self.delete_directory("./"+ downloaded_project_path +'/')
                    except:
                        pass
        try:
            self.delete_directory("./"+ git_projects +'/')
        except:
            pass
    def run(self):
        global is_currently_updating
        is_currently_updating = True
        self.update()
        is_currently_updating = False


class HandleRequests(BaseHTTPRequestHandler):
    web_app_root = os.getcwd()

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        routes = ["/", "/status", "/update"]

        if self.path == routes[0]:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            index = open(self.web_app_root+"/index.html","rb")
            self.wfile.write(index.read())

        elif self.path == routes[1]:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            global is_currently_updating
            self.wfile.write(is_currently_updating)
        
        elif self.path == routes[2]:
            # self.send_response(302)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            # self.send_header('Location', routes[0])
            self.end_headers()
            if (not is_currently_updating):
                LocalMavenRepositoryUpdater().start()
            self.wfile.write("")

        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write("Page not found.")

def main():
    PORT = 80
    print("Serving at port " + str(PORT))
    web_server = HTTPServer(("", PORT), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()