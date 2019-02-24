# What is BabelFish? 

BabelFish is an open source package that can be used to convert any language's source code into a universal abstract syntax tree. This tree will be used with the ast2vec package. [The homepage can be found here](https://doc.bblf.sh/).

#Getting Started

In this directory you will find two shell scripts. You may need to install docker if you don't already have it in order for them to work. [You can find Docker here](https://docs.docker.com/install/). 

Once you have that installed, first run 

```
./bblfsh_client.sh
```

This will start a daemon process. While this is running, run 

```
./bblfsh_driver.sh
```

You only need to run the driver once! This will install all the different language drivers that can be used for creating universal abstract syntax trees. 

#Regular Usage

Make sure you have `./bblfsh_client.sh` running. 

To test something out, go ahead and run 

```
python3 ast.py parseDate.py 
```

or 

```
python3 ast.py Factorial.java
```

Running either one of these will print out the universal abstract syntax tree.   
