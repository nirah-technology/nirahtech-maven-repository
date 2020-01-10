import os
import sys
import re
import shutil
import time

def are_valid_arguments(ARGUMENTS):
    if (len(ARGUMENTS) == 2):
        if (str(ARGUMENTS[-1]).endswith(".jar")):
            return True
    return False

def extract_artifact_id_and_version(url):
    splited_path = str(str(url).replace("\\", "/").replace("//", "/").replace("//", "/")).split("/")
    jar_file = str(splited_path[-1])
    if (jar_file.endswith(".jar")):
        jar_file = jar_file.replace(".jar", '')
        # json-geco-0.0.1-SNAPSHOT
        informations = jar_file.split('-')
        VERSION = re.search(r'([0-9]){1,}([.]([0-9]){1,}){0,}.+',jar_file).group(0)
        ARTIFACT_ID = jar_file.replace("-"+VERSION, '')
        return {"artifact": ARTIFACT_ID, "version": VERSION}
    exit(1)

def execute_maven_command(url, data):
    maven_install_command = "mvn install:install-file -DgroupId=io.nirahtech -DartifactId="+data["artifact"]+" -Dversion="+data["version"]+" -Dfile="+url+" -Dpackaging=jar -DgeneratePom=true  -DcreateChecksum=true"
    os.system(maven_install_command)

def process():
    ARGUMENTS = sys.argv
    if (are_valid_arguments(ARGUMENTS)):
        # Manual
        URL = str(ARGUMENTS[1])
        data = extract_artifact_id_and_version(URL)
        execute_maven_command(URL, data)
        return

    # Automatic: PROS-WORKSTATION-WINDOWS
    workspace_root_base = "C:\\Users\\nmetivier\\Documents\\Programmation\\NIRAHTECH\\Java\\"
    
    # Automatic: PROS-WORKSTATION-LINUX
    # workspace_root_base = "/mnt/c/Users/nmetivier/Documents/Programmation/NIRAHTECH/"
    
    # Automatic: NIRAH-WORKSTATION-WINDOWS
    # workspace_root_base = str(ARGUMENTS[1])
    
    # Automatic: NIRAH-WORKSTATION-LINUX
    # workspace_root_base = str(ARGUMENTS[1])
    
    # Automatic: NIRAH-LAPTOP-LINUX
    # workspace_root_base = str(ARGUMENTS[1])

    workspace_root_base = workspace_root_base.replace("\\", "/").replace("//", "/").replace("//", "/")
    projects = os.listdir(workspace_root_base)
    for project in projects:
        url = str(str(workspace_root_base) + str(project) + "/target/")
        if (os.path.exists(url) and os.path.isdir(url)):
            for potential_jar_file in os.listdir(url):
                if (str(potential_jar_file).endswith(".jar")):
                    url = str(url + str(potential_jar_file))
                    data = extract_artifact_id_and_version(url)
                    execute_maven_command(url, data)

def download_or_update():
    github_project_url = "https://github.com/nirah-technology/nirahtech-maven-repository.git"
    project_name = github_project_url.split('/')[-1].replace(".git", '')
    if (os.path.exists("./"+project_name)):
        os.chdir("./"+project_name)
        print("Must be updated!")
        os.system("git pull origin repository")
    else:
        print("Must be downloaded!")
        os.system("git clone " + github_project_url)
        os.chdir("./"+project_name)

def updload():
    os.system("git add .")
    os.system('git commit -m "Update libraries"')
    os.system("git push origin repository")
    os.chdir("..")

def main():
    download_or_update()
    process()
    updload()


if __name__ == "__main__":
    main()