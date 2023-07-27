# 0x04. AirBnB clone - Web framework

## General
- What is a Web Framework?
- How to build a web framework with Flask.
- How to define routes in Flask.
- What is a route?
- How to handle variables in a route.
- What is a template?
- How to create an HTML response in Flask by using a template.
- How to create a dynamic template (loops, conditions...).
- How to display data from a MySQL database in HTML.

## Project Overview
The **"0x04. AirBnB Clone - Web Framework"** project aims to develop a web framework using Flask, a lightweight Python web framework. The goal is to build a fully functional web application capable of defining routes, handling variables, using templates for dynamic HTML responses, and displaying data from a MySQL database. The project adheres to strict coding standards and includes comprehensive documentation.

## Requirements

### Python Scripts
- Allowed editors: vi, vim, emacs.
- All your files will be interpreted/compiled on Ubuntu 20.04 LTS using python3 (version 3.4.3).
- All your files should end with a new line.
- The first line of all your files should be exactly `#!/usr/bin/python3`.
- A `README.md` file, at the root of the folder of the project, is mandatory.
- Your code should use the **PEP 8 style (version 1.7)**.
- All your files must be executable.
- The length of your files will be tested using `wc`.
- All your modules should have documentation (`python3 -c 'print(import("my_module").doc')`).
- All your classes should have documentation (`python3 -c 'print(import("my_module").MyClass.doc')`).
- All your functions (inside and outside a class) should have documentation (`python3 -c 'print(import("my_module").my_function.doc')` and `python3 -c 'print(import("my_module").MyClass.my_function.doc)'`).
- A documentation is not a simple word, it's a real sentence explaining what's the purpose of the module, class, or method (the length of it will be verified).

### HTML/CSS Files
- Allowed editors: `vi, vim, emacs`.
- All your files should end with a new line.
- A `README.md` file at the root of the folder of the project is mandatory.
- Your code should be W3C compliant and validate with W3C-Validator (except for jinja template).
- All your CSS files should be in the styles folder.
- All your images should be in the images folder.
- You are not allowed to use `!important` or `id (#... in the CSS file)`.
- All tags must be in uppercase.
- Current screenshots have been done on Chrome 56.0.2924.87.
No cross browsers.

## Installation
To install Flask, use the following command:
```bash
$ pip3 install Flask
```

## Project Structure
The project is organized into the following directories and files:
```bash
web_flask/
    ├── example_script.py
    ├── __init__.py
    ├── static/
    │   ├── styles/
    │   │   ├── style.css
    │   │   └── ...
    │   └── images/
    │       ├── image1.jpg
    │       └── ...
    ├── templates/
    │   ├── base.html
    │   └── ...
    └── README.md
```

## Description
The **0x04. AirBnB Clone - Web Framework** project aims to build a web framework using Flask, a lightweight Python web framework. The web framework will facilitate the creation of a fully functional web application with features such as defining routes, handling variables, using templates for dynamic HTML responses, and displaying data from a MySQL database.

The project strictly adheres to coding standards and best practices. It includes comprehensive documentation for all modules, classes, and functions to ensure clarity and maintainability of the codebase.

## Usage
To run the Flask web application, execute the `example_script.py` script:
```bash
$ ./example_script.py

```

The application will start running on a local development server, and you can access it by visiting **http://localhost:5000** in your web browser.

## Web Application Features
The web application built with Flask provides the following features:

**Defining routes:** Routes are defined in the `app.py` script using decorators. Each route corresponds to a specific URL, and Flask triggers the appropriate function when the URL is accessed.

**Handling variables in routes:** Flask allows you to handle variables in routes by using angle brackets `<variable_name>` in the route definition. These variables can then be accessed as arguments in the corresponding route function.

**Using templates:** Flask supports the use of templates for generating dynamic HTML content. `The templates/` directory contains HTML templates that can include placeholders for dynamic data.

**Displaying data from a MySQL database:** The web application connects to a MySQL database and retrieves data to display on the web pages. The data is integrated into the HTML templates using Flask's template engine.
ruby

## Conclusion
The **0x04. AirBnB Clone - Web Framework** project provides a solid foundation for building web applications in Python. It encompasses essential aspects of web development, including route handling, template rendering, and database integration, allowing developers to create dynamic and interactive web applications with ease.
