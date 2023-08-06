<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]




<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Panchitoz1/luanspaceship">
    <img src="images/logo.png" alt="Logo" width="122" height="233">
  </a>



<h3 align="center">Luan Spaceship</h3>

  <p align="center">
    A simple Python Command-Line Interface script that prints a variable-size spaceship!
    <br />
    <a href="https://github.com/Panchitoz1/luanspaceship"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Panchitoz1/luanspaceship">View Demo</a>
    ·
    <a href="https://github.com/Panchitoz1/luanspaceship/issues">Report Bug</a>
    ·
    <a href="https://github.com/Panchitoz1/luanspaceship/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#installation">Installation</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installing">Installing</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://github.com/Panchitoz1/luanspaceship)

Luanspaceship is a really simple Command-Line Interface written in Python3 that prints an ASCII spaceship in function of a length given via flag. Aditionally, output can be copied into clipboard, change colors of spaceship printed (only for console visual purposes) and a couple of others functions.

This is a little project written for [Science & Commit // Workshop 2022](https://github.com/Science-and-Commit/Workshop_2022).


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Installation


This simple project needs a few Python3 packages to run properly.

### Prerequisites


* <b>pip</b> (if you have already installed <b>pip</b> you can ignore this subsection) 

  If for some reason you have not installed <b>pip</b> with Python3 (which would be... weird) try this: 
  
  - Download the script, from [https://bootstrap.pypa.io/get-pip.py](https://bootstrap.pypa.io/get-pip.py)

  - Open a terminal/command prompt, `cd` to the folder containing the <b>get-pip.py</b> file and run

    On Linux/MacOS:
    ```
    python3 get-pip.py
    ```
    On Windows:
      ```
      py get-pip.py
      ```
    
    For more options you can also check [official Python 'pip' documentation](https://pip.pypa.io/en/stable/installation/).


### Installing

* Option 1: <b>pip install</b>
  ```sh
   pip install luanspaceship
   ```
  
* Option 2: Install manually
1. Clone the repo
   ```sh
   git clone https://github.com/Panchitoz1/luanspaceship.git
   ```
2. Ensure <b>setuptools</b> package is updated: 
    ```sh
    python3 -m pip install --upgrade setuptools
    ```
3. Install using <b>setup.py</b>
   ```sh
   python3 setup.py install
   ```
   This should also install all package-dependences and program should run without problems.
   
4. (Optional to fix 'Module error') If for some reason when run the program in terminal Python returns a Module error due to some packages not being found, try this:

    - Ensure you are in the repo directory:
       ```sh
       cd /path/to/repo/LuanSpaceship
       ```

       Once there, simply run:
        ```sh
        pip install -r requirements.txt
        ```
      and try re-running command from Step 3.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

First of all you can type in your terminal the following command:
```sh
luanspaceship
```
If everything runs fine it should print an ASCII spaceship with length 5 (which is default value if `-length` flag is not provided).


For general purposes to print an ASCII spaceship of length `<integer-number>` we can simply run:
```sh
luanspaceship -length <integer-number>
```

Another example could be if you want to print an ASCII spaceship with length 8 and also want to copy the ASCII art result into your clipboard:
```sh
luanspaceship -length 8 -clipboard
```
You can also change color combinations using `-colorstyle` flag and/or adding some attributes/styles when being displayed with `-style` flag. For example:
```sh
luanspaceship -colorstyle ocean -style blink
```
To check all flags and functions available I recommend check short help-page running:
```sh
luanspaceship -h
```

[![Product Name Gif][product-gif]](https://github.com/Panchitoz1/luanspaceship)


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. Check [LICENSE](https://github.com/Panchitoz1/luanspaceship/blob/main/LICENSE) file for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Francisco Carrasco Varela - email: ffcarrasco@uc.cl

Project Link: [https://github.com/Panchitoz1/luanspaceship](https://github.com/Panchitoz1/luanspaceship)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Science & Commit // Workshop 2022](https://github.com/Science-and-Commit/Workshop_2022)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Panchitoz1/luanspaceship.svg?style=for-the-badge
[contributors-url]: https://github.com/Panchitoz1/luanspaceship/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Panchitoz1/luanspaceship.svg?style=for-the-badge
[forks-url]: https://github.com/Panchitoz1/luanspaceship/network/members
[stars-shield]: https://img.shields.io/github/stars/Panchitoz1/luanspaceship.svg?style=for-the-badge
[stars-url]: https://github.com/Panchitoz1/luanspaceship/stargazers
[issues-shield]: https://img.shields.io/github/issues/Panchitoz1/luanspaceship.svg?style=for-the-badge
[issues-url]: https://github.com/Panchitoz1/luanspaceship/issues
[license-shield]: https://img.shields.io/github/license/Panchitoz1/luanspaceship.svg?style=for-the-badge
[license-url]: https://github.com/Panchitoz1/luanspaceship/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[product-gif]: images/usage_example.gif