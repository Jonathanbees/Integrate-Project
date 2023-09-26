# Tendeus
Welcome to the *Tendeus* GitHub repository! 

## Context of the project

Tendeus is an innovative online retail platform dedicated to bolstering a local business, enhancing their profitability, and expanding their customer reach. This project was conceived with the goal of revitalizing the local economy by putting together the power of e-commerce and digital marketing.

Tendeus represents a bridge between traditional local businesses and the digital age, creating a win-win situation where local economies flourish, and consumers gain access to a wider array of products and services. By leveraging the power of technology, this project has the potential to make a lasting positive impact on communities while propelling local businesses toward sustained growth and success.

*This project requires several libraries and programs to run successfully. Please follow the instructions below to set up your environment and run the program.*

## Programs required
Before you begin, make sure you have the following libraries and programs installed:

### Download Visual Studio Code:
- Open your web browser and go to the official Visual Studio Code website at https://code.visualstudio.com/.
- Click on the "Download" button to download the installer. Click the "Next" button to proceed with the installation.
- Click "Install" to start the installation process.

### Download Python:
- Visit the official Python website at https://www.python.org/downloads/windows/.
- Download the latest Python installer for Windows by clicking on the "Download Python" button in the version that you prefer
- Click the "Install Now" button to start the installation process. The installer will copy Python files to your system.
- Open the Command Prompt or PowerShell and type the command
~~~
python --version
~~~
This is to make sure that you installed it succesfully

### Download Mysql:
- Visit the official mysql website at https://dev.mysql.com/downloads/installer/
- Select the version of the mysql that you want to install
- Follow the instructions of the installation wizard
- *Note: During the installation process, you will be prompted to set a root password for MySQL. Make sure to remember this password as you'll need it later.*

### Clone the github repository:
- Open your web browser and go to https://github.com.
- Log in to your GitHub account or register if you didn´t have one yet
- Into the Command Prompt or Powershell run:
~~~  
git clone https://github.com/Jonathanbees/Integrate-Project
~~~
This will charge all the files of the repository into the folder that you select on the command prompt after

## Libraries required

- Django
- Pillow
- Jazzmin
- Mysqlclient
- MySQL-Mysql Workbench

### Install Pillow:
  - In the command prompt, put the following code:
  ~~~
  pip install pillow
  ~~~
    
### Install jazzmin:
  - In the command prompt, put the following code:
  ~~~
  pip install jazzmin
  ~~~
    
### Install mysqlclient:
  - In the command prompt, put the following code:

  ~~~
  pip install mysqlclient
  ~~~
    
## Instructions to Run the Program
Follow these steps to set up and run the program:

1. Configure MySQL Connection:

  - Open MySQL Workbench.
  - Create a new connection with the parameters that you want. Ensure that these parameters match the settings specified in the settings.py file for the database connection.
2. Initialize the Database:

  - In this repository, you will find an SQL file. Open this SQL file in MySQL Workbench.

3. Run the Django Application:

  - Open your command prompt or terminal.
  - Navigate to the project folder that you previously set up.
    
4. Execute the Django Server:

  - Run the following command to start the Django development server:
~~~
python manage.py runserver
~~~
5. Access the Application:

  - Once the server is running, open your web browser and go to http://localhost:8000 (or the address provided by Django).
That's it! You have successfully set up and executed the program. If you encounter any issues or have further questions, please refer to the wiki or reach out to our support team.

Thank you for using *Tendeus*. Happy coding! 😊

### Contributors:
- Jonathan Betancur
- Santiago Gómez
- Juan José Hernández
