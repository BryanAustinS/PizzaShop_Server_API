# Tools used in the project
The following lists the tools and frameworks, that are used in the project. 
- [Docker](https://docs.docker.com/get-started/overview/)    
   Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker's methodologies for shipping, testing, and deploying code, you can significantly reduce the delay between writing code and running it in production.
- [Kubernetes](https://kubernetes.io/docs/concepts/overview/)
- [FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [FastAPI with SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)

# GitLab CI/CD

The following is a collection of short hints on how to do the most essential things in a GitLab CI/CD pipeline:

- How to delay a job until another job is done: use 'needs'
    
- How to change the image used in a task: specify the 'image' keyword at the job level to use a different Docker 
  image for a specific job
    
- How do you start a task manually: use 'when' with the vale 'manual'

- The Script part of the config file - what is it good for?

    to define the command or series of commands of the job executes

- If I want a task to run for every branch I put it into the stage ?? Type in:
    stage: build

- If I want a task to run for every merge request I put it into the stage ??
Add a new stage specifically for merge requests, and insert the task here. In this stage, add the keyword: "only: merge_requests"
- If I want a task to run for every commit to the main branch I put it into the stage ?? Then in the yaml file, type in:
rules:
  - if: '$CI_COMMIT_BRANCH == "main"'



# flake8 / flakeheaven

- What is the purpose of flake8?
  The purpose of flake8 is to ensure quality of the code in terms of its consistency and could catch potential issues

- What types of problems does it detect
  It detects style violations for example indentation, and errors in programming such as syntax errors, and logical errors

- Why should you use a tool like flake8 in a serious project?
So that the code can be consistently high quality which helps other programmers to understand the code

## Run flake8 on your local Computer

  It is very annoying (and takes a lot of time) to wait for the pipeline to check the syntax 
  of your code. To speed it up, you may run it locally like this:

### Configure PyCharm (only once)
- select _Settings->Tools->External Tools_ 
- select the +-sign (new Tool)
- enter Name: *Dockerflake8*
- enter Program: *docker*
- enter Arguments: 
    *exec -i 1337_pizza_web_dev flakeheaven lint /opt/project/app/api/ /opt/project/tests/*
- enter Working Directory: *$ProjectFileDir$*

If you like it convenient: Add a button for flake8 to your toolbar!
- right click into the taskbar (e.g. on one of the git icons) and select *Customize ToolBar*
- select the +-sign and Add Action
- select External Tools->Dockerflake8

### Run flake8 on your project
  - Remember! You will always need to run the docker container called *1337_pizza_web_dev* of your project, to do this! 
    So start the docker container(s) locally by running your project
  - Now you may run flake8 
      - by clicking on the new icon in your toolbar or 
      - by selecting from the menu: Tools->External Tools->Dockerflake8 

# GrayLog

- What is the purpose of GrayLog?
  - monitoring, searching, and analyzing log data, allowing users to gain insights into their systems and applications, detect issues, and ensure security and compliance.

- What logging levels are available?
  - DEBUG, INFO, WARNING, ERROR, CRITICAL

- What is the default logging level?
  - WARNING

- Give 3-4 examples for logging commands in Python:
  ```python
    logging.debug()
    logging.warning()
    logging.info()
  ```

# SonarQube

- What is the purpose of SonarQube?
  - to check code smell and bug

- What is the purpose of the quality rules of SonarQube?
    To ensure the quality and maintainability of the codebase, and to maintain consistency within the code to prevent further bugs or code smells that may appear.
- What is the purpose of the quality gates of SonarQube?
    Quality gates determines if our project is ready to release or not according to the conditions that we set, 
    for example if the code has no issues left or when the code coverage on new code is greater than 80%

## Run SonarLint on your local Computer

It is very annoying (and takes a lot of time) to wait for the pipeline to run SonarQube. 
To speed it up, you may first run the linting part of SonarQube (SonarLint) locally like this:

### Configure PyCharm for SonarLint (only once)

- Open *Settings->Plugins*
- Choose *MarketPlace*
- Search for *SonarLint* and install the PlugIn

### Run SonarLint

- In the project view (usually to the left) you can run the SonarLint analysis by a right click on a file or a folder. 
  You will find the entry at the very bottom of the menu.
- To run it on all source code of your project select the folder called *app*

# VPN

The servers providing Graylog, SonarQube and your APIs are hidden behind the firewall of Hochschule Darmstadt.
From outside the university it can only be accessed when using a VPN.
https://its.h-da.io/stvpn-docs/de/ 

### Docker

Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker's methodologies for shipping, testing, and deploying code, you can significantly reduce the delay between writing code and running it in production.

### Kubernetes

Kubernetes is a portable, extensible, open source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation. It has a large, rapidly growing ecosystem. Kubernetes services, support, and tools are widely available.

Kubernetes provided:

- **Service discovery and load balancing** Kubernetes can expose a container using the DNS name or using their own IP address. If traffic to a container is high, Kubernetes is able to load balance and distribute the network traffic so that the deployment is stable.
- **Storage orchestration** Kubernetes allows you to automatically mount a storage system of your choice, such as local storages, public cloud providers, and more.
- **Automated rollouts and rollbacks** You can describe the desired state for your deployed containers using Kubernetes, and it can change the actual state to the desired state at a controlled rate. For example, you can automate Kubernetes to create new containers for your deployment, remove existing containers and adopt all their resources to the new container.

### Fast API

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints.

The key features are:

- **Fast**: Very high performance, on par with **NodeJS** and **Go** (thanks to Starlette and Pydantic).
- **Fast to code**: Increase the speed to develop features by about 200% to 300%. *
- **Fewer bugs**: Reduce about 40% of human (developer) induced errors. *
- **Intuitive**: Great editor support.  everywhere. Less time debugging.
    
    Completion
    
- **Easy**: Designed to be easy to use and learn. Less time reading docs.
- **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.
- **Robust**: Get production-ready code. With automatic interactive documentation.

### SQL Alchemy

SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.

### Fast API with SQL Alchemy

Can easily adapt it to any database supported by SQLAlchemy, like:

- PostgreSQL
- MySQL
- SQLite
- Oracle
- Microsoft SQL Server, etc.

### Alembic

Alembic provides for the creation, management, and invocation of *change management* scripts for a relational database, using SQLAlchemy as the underlying engine. This tutorial will provide a full introduction to the theory and usage of this tool.

### Swagger UI

Swagger UI allows anyone — be it your development team or your end consumers — to visualize and interact with the API’s resources without having any of the implementation logic in place. It’s automatically generated from your OpenAPI (formerly known as Swagger) Specification, with the visual documentation making it easy for back end implementation and client side consumption.

add beverage to order ( di order endpoints) and create beverage is different