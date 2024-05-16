# Book Plus Library Management System

README - Book Plus Web Application Setup

Refer to the tutorial if you hate reading -> https://drive.google.com/file/d/15SGeTkKg_w9A50JzIn1XJbBFTS_Bsf5A/view?usp=sharing

This guide provides step-by-step instructions on how to set up and run this Flask web application. Follow the steps below to get started:

-> Prerequisites
	Before proceeding with the installation, ensure that you have the following prerequisites:

->> Python: Install Python (3.10) on your system. You can download Python from the official website: python.org.

->> Pip: Install Pip, the package installer for Python. Pip is usually bundled with Python, so you should have it available after installing Python. You can verify its installation by running pip --version in your command prompt or terminal.

->> Code Editor: Install a code editor of your choice. I recommend using Visual Studio Code (VS Code), which can be downloaded from the official website: code.visualstudio.com.

-> Setup Instructions
	Follow these steps to set up and run the Flask-VueJS web application:

->> Download: Download the project folder and unzip it to your preferred location.

->> Open Project Folder: Open the project folder named 'Code' in your chosen code editor (e.g., VS Code). You should see the project's files and folders within the editor.

->> Terminal Setup: Open a command prompt within your code editor.
->> Install virtualenv: In the command prompt, run the following command to install virtualenv:

pip install virtualenv

->>Create Virtual Environment: After the successful installation of virtualenv, create a virtual environment by running the following command:

cmd(windows):
virtualenv <name_of_env>

bash(linux):
python3 -m virtualenv <name_of_env>

Replace <name_of_venv> with a suitable name for your virtual environment.

->> Activate Virtual Environment: Navigate to the virtual environment's scripts folder by running the following commands in the command prompt or terminal & install all the packages required to run this applcation.:

cmd(windows):
cd <name_of_env>/Scripts
activate
cd ../.. OR cd.. (x2)
pip install -r requirement.txt

bash(linux):
source <name_of_env>/bin/activate
pip install -r requirement.txt


The virtual environment is now activated, and you should see (name_of_env) in your command prompt or terminal.

->> Run the Application Step-1: Start the Backend Flask web application by running the following command in the command prompt or terminal:

cmd(windows)
cd Backend
python app.py

bash(ubuntu)
cd Backend
flask run

->> Run the Application Step-2: Start the Frontend VueJs by running the following command in the command prompt or terminal:

cd Frontend/book_plus
npm init
npm install
npm run serve

->> Run the Application Step-3: Start the Task Scheduling by running the following command in the command prompt or terminal:

!! Redis Must Be Installed - https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/

celery -A tasks worker --loglevel=info 

->> Access the Application: Open your preferred web browser and type localhost:5000 in the address bar. The web application should now be running, and you can interact with it.

Congratulations! You have successfully set up and run the application. Enjoy exploring its features and functionality.

-------------*-------------*--------------*--------------*---------------

If you encounter any issues or have further questions, please contact ktrzorion@gmail.com or 21f1004160@ds.study.iitm.ac.in.

Thank you for using my application!
