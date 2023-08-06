# RemotePyLib

This is a package to use Nalin Angrish's - RemotePyLib API.  

It's Official Website: [Visit](http://www.nalinangrish.me/apps/remotepylib)  
It's Official GitHub Page: [Visit](https://github.com/Nalin-Angrish/RemotePyLib)  
It's Official PyPi Page: [Visit](https://pypi.org/project/RemotePyLib/)  
(It's Release History: [Visit](https://pypi.org/project/RemotePyLib/#history))



## Usage

Firstly, you would have to install this package. To do so open up your Terminal/Command Prompt and type:

```shell
pip install RemotePyLib
```



Secondly, you would have to upload a module to the Nalin Angrish's RemotePyLib API.

If you want to do so manually, go to the official website. Else if you wish to do so programmatically, follow the steps:

- Create a python file to be exported in the directory of your main file.

- In your main file, import the exporting class by: 

  ```python
  from RemotePyLib import Exporter
  ```

- create and instance of the exporter object by:

  ```python
  exporter = Exporter()
  ```

- upload a file and get the key by:

  ```python
  key = exporter.exportFile('myTestFile', 'modulename', 'myEmail@example.com')
  ```

- the key should be kept secure so just print it by:

  ```python
  print(key)
  ```

- Or if you have a string value instead of a python file to be uploaded, replace

  ```python
  key = exporter.exportFile('myTestFile', 'modulename', 'myEmail@example.com')
  ```

  With

  ```python
  key = exporter.exportString('StringValue', 'modulename', 'myEmail@example.com')
  ```

  

  Note that this key will also be sent to the email address and if the email address is not valid, it will raise an InvalidEmailError (scroll down for reference) and if the email couldn't be reached, then the module uploaded will be taken down soon. Also, if the modulename already exists, then an ExportError (scroll down for reference) will be raised.

Here, the modulename and the key will be used to import/execute the remote modules.



Thirdly, You would have to import and use the module.

Follow the below steps:

- import the importer class by:

  ```python
  from RemotePyLib import Importer
  ```

- create an instance of the importer object by:

  ```python
  importer = Importer()
  ```

- If your module is a script and does not need to be imported, use:

  ```python
  importer.execModule('modulename', 'my_key')
  ```

- Or if your module is needed to be imported, use:

  ```python
  module = importer.importModule('modulename', 'my_key')
  ```

- If you have imported the module you can use it's functions and attributes by:

  ```python
  module.func(parameter1, parameter2, .....)
  value = module.variable
  myClass = module.MyClass()
  ```

If stuck, refer to the documentation below or add an issue in the issues section of the GitHub page

### Classes

> Importer
##### Desc.: 
A class to remotely import packages using Nalin Angrish's RemotePyLib API.

##### Functions:
- execModule(self, modulename, key)  
This method is used to execute the remote module on the local machine.  

        Args:
            modulename (str): name of the module you have uploaded (The name is not surely the name of the python file you have uploaded. You would have entered a specific name in the 'name of module field' of the website).
            key (str): The access key given to you after you have uploaded the python module.
        Usage:
            importer = Importer()
            importer.execModule('module', 'key')  

- importModule(self, modulename, key)  
This method is used to import the remote module as a standard module.  
The classes and methods inside the remote module will work as if there was another python file along.  
Note that there should not be any python file with the same name as 'modulename' otherwise all the data in that file will be cleared.  
It returns the module object for the imported module.  

        Args:
            modulename (str): name of the module you have uploaded (The name is not surely the name of the python file you have uploaded. You would have entered a specific name in the 'name of module field' of the website).
            key (str): The access key given to you after you have uploaded the python module.
        Usage:
            importer = Importer()
            module = importer.importModule('module', 'key')
            module.func()
            var = module.variable
            myClass = module.myClass()
> Exporter  
##### Desc.:
A class to export custom libraries to Nalin Angrish's - RemotePyLib API.

##### Functions:
- exportFile(self, filepath, modulename, email)  
  Export a python file to the Nalin Angrish's API.  
  Returns the access key.  
  Please keep the access key with you because it is required for importing the library. In case lost, contact the owner (go the the website and contact using email).
        

        Args:
            filepath (str): path of the python file to be uploaded.
            modulename (str): name of the module with which it can be imported later.
            email (str): email address to recieve the key. If found invalid, then the module uploaded will be taken down.
        Usage:
            exporter = Exporter()
            key = exporter.exportFile('/mymodule.py', 'modulename', 'myemail@example.com')
            print(key)

- exportString(self, content, modulename, email)  
Creates a remote library on Nalin Angrish's - RemotePyLib API.  
It returns the access key.  
Please keep the access key with you because it is required for importing the library. In case lost, contact the owner (go the the website and contact using email).
        
        Args:
            content (str): content to be placed in the remote library.
            modulename (str): name of the module with which it can be imported later.
            email (str): email address to recieve the key. If found invalid, then the module uploaded will be taken down.
        Usage:
            exporter = Exporter()
            key = exporter.exportString('print("Hello World!")', 'modulename', 'myemail@example.com')
            print(key)        


### Exceptions
> InvalidAccessError
##### cause:
Thrown when the key entered to access the remote module is incorrect.
##### solution:
Check the access key and try again.  

> RemoteModuleNotFoundError
##### cause:
Thrown when the name of the remote module to be imported could not be found.
##### solution:
Check the name of the module that is to be imported and try again.  

> ExportError
##### cause:
Thrown when the module could not be exported because another module with the same name was present on the server.
##### solution:
Try exporting the module using another name.

> InvalidEmailError
##### cause:
Thrown when the email entered to upload the module using exporter is not valid.
##### solution:
Check the email address and try again.
