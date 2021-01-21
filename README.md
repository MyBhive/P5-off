## ***[]()PURBEURRE APP***

> USE PUBLIC DATA FROM OPENFOODFACTS

`Uses:`

- Run the program

- Download 10 specifics categories (and 1000 products for each categories) from the Open Food Facts API
- Insert into the "purbeurre" database created for it
- The program will asks the user if he wants to look for a product and find a better alternative of it (substitute), or to check the substitute already saved (if there is any).
- The user will have to choose a category depending of the category's number
- The user will have to choose a product out of 10 random one proposed
- A substitute will be suggest if any better product is existing
- The user will choose to save the substitute in the database or not

---------------------------------------------------------------------------------------------

[]()**RUN THE PROGRAM:**

`Installation required:`

- Install Virtual Environment : python -m pip install --user virtualenv
- Install "mysql" and "pyyaml"
- Open the file "install.py" to install all the necessary package
  !! Don’t forget to run cmd or powershell as administrator !
- put your own "user" and "password" in the "authentification.yaml" file to run the program

`Launch:`

- To start the app after that, launch main.py


----------------------------------------------------------------------------------------------

[]()**FEATURES:**

`Encoding:`
Python 3

`Fork:`
https://github.com/MyBhive/P5-off

-----------------------------------------------------------------------------------------------

[]()**DESCRIPTION:**

`Folder`

| p5off | Contain all the code |
| ----- | -------------------- |
|       |                      |

`Python files`

| **Install.py** | file to install “requirement.txt”      |
| -------------- | -------------------------------------- |
| cursor.py**    | all the code necessary for the program |
| main.py**      | file to run the program                |

`Text files`

| authentification.yaml | login for the database                                   |
| --------------------- | -------------------------------------------------------- |
| Requirement.txt       | package to download with "install.py" to run the program |

----------------------------------------------------------------------------------------------

[]()**TO CONTRIBUTE:** 

> You need to respect PEP8 !!!  

- Fork it 

- Create your feature branch

- Commit your changes

- Push to your branch 

- Create a pull request

-----------------------------------------------------------------------------------------------

##### []()**WRITTEN BY:**

> MyBhive 

*My most sincere thanks to Abdelhamid for his time and wise advices and  to Geoffrey for his support.*