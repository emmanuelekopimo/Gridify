import os, sys, secrets, webbrowser
import shutil
from zipfile import ZipFile 

zip_file = sys.argv[1]

def list_files_in_folder(folder_path):
    """
    Lists all files and subfolders within a given folder.

    Parameters:
    - folder_path: Path to the folder

    Returns:
    - List of file and subfolder names
    """
    files = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if os.path.isfile(os.path.join(dirpath, filename)):
                files.append(os.path.relpath(os.path.join(dirpath, filename), os.path.join('projects', project_name)))
    return files

if getattr(sys, 'frozen', False):
    # Running in PyInstaller bundle
    script_dir = sys._MEIPASS
else:
    # Running as a Python script
    script_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(script_dir)
# Get the name of the project
project_name = secrets.token_hex(10)


# Copy the content of the web folder to the project folder so they can now be modied
shutil.copytree('web', os.path.join('projects',project_name))

# Unzip the package
with ZipFile(zip_file, 'r') as zObject: 
    # Extracting all the members of the zip  
    # into a specific location. 
    zObject.extractall(path=os.path.join('projects', project_name,'res')) 

# Get list of images
    
all_images = list_files_in_folder(os.path.join('projects', project_name,'res'))
# Create html content with the image names
new_content = ''
for image in all_images:
    new_content += '<img src="'+image+'" alt="Slide" class="slide">\n'

# Modify the index.html
with open('web/index.html', 'r')as html:
    html_content = html.read()
    _ = html_content.replace('*slides_list*', new_content)
    new_content_html = _.replace('*project_name*', project_name)

with open('projects/'+project_name+'/index.html','w')as html:
    html.write(new_content_html)

# Print out locations of the images
print(os.path.abspath(os.path.join('projects', project_name,'res')))

# Finally open the generated web page

webbrowser.open(os.path.abspath(os.path.join('projects', project_name,'index.html')))
