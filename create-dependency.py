import os
import sys
import re

def are_valid_arguments(ARGUMENTS):
    if (len(ARGUMENTS) == 2):
        if (str(ARGUMENTS[1]).endswith(".jar")):
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
    maven_install_command = "mvn install:install-file -DgroupId=io.nirahtech -DartifactId="+data["artifact"]+" -Dversion="+data["version"]+" -Dfile="+url+" -Dpackaging=jar -DgeneratePom=true -DlocalRepositoryPath=.  -DcreateChecksum=true"
    os.system(maven_install_command)


def process(ARGUMENTS):
    if (are_valid_arguments(ARGUMENTS)):
        URL = str(ARGUMENTS[1])
        data = extract_artifact_id_and_version(URL)
        execute_maven_command(URL, data)
        return
    print("ERROR: Arguments not valid. A path that point to a '.jar' file is required.")

def main():
    ARGUMENTS = sys.argv
    process(ARGUMENTS)
    

if __name__ == "__main__":
    main()