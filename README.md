#  Outflow from the spin-induced offset stream self-crossing shocks in TDEs

<div id="top"></div>
<!--
*** README template is from: https://github.com/othneildrew/Best-README-Template
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
 <!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]
  [![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="Figures/dz1.2_rho_phys_no_colorbar.png" alt="Logo" width="250" height="250">
       <img src="Figures/normalized_healpix_map_of_F_dz=1.20_nside=64_same_limits_lmaxsmooth=40_smooth_fwhm=0.05_symm.png" alt="Logo" width="475" height="250">

  </a>

  <h3 align="center">Spin-induced offset stream self-crossing shocks in tidal disruption events</h3>

  <p align="center">
    Calculate the outflow from the self-crossing region like never before!
    <br />
     <!-- <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>  -->
    <br />
    <br />
   <!-- <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>  -->

[Report a bug](https://github.com/tajjankovic/Spin-induced-offset-stream-self-crossing-shocks-in-TDEs/issues).

  
 <!--   <a href="issues">Request Feature</a>  -->
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
               <li><a href="#Built-with">Built With</a></li>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
         <li><a href="#basic-steps">Basic Steps</a></li>
         <li><a href="#running-the-program">Running the program</a></li>
      </ul>
    </li>
   <!-- <li><a href="#roadmap">Roadmap</a></li> -->
  <!--   <li><a href="#contributing">Contributing</a></li> -->
  <!--   <li><a href="#license">License</a></li> -->
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com)  -->

<!--  In recent years, there have been several studies related to numerical simulations of TDEs ([[1]](#1), [[2]](#2), [[3]](#3), [[4]](#4), [[5]](#5), [[6]](#6)).  -->
Tidal disruption events occur at the center of a galaxy when a star is disrupted in the supermassive black hole’s tidal field.
Following the disruption, approximately half of the elongated stream of debris returns to the black hole’s vicinity. Due to
relativistic apsidal precession, the part of the stream that passed pericenter collides with the still-infalling gas, leading to a
self-crossing shock that triggers accretion disk formation. If the black hole spins, the additional Lense-Thirring precession
induces an offset between these two colliding components that can affect the outcome of the interaction. We study this effect
of the black hole’s spin by locally simulating collisions between two streams, which are offset in the direction perpendicular
to their orbital plane. 

We have simulated 21 stream collisions corresponding to values of the offset $\Delta z \in [0, 1.8H]$, with an increment of $0.1H$, where $H$ is the stream height, and calculated the outflow rate in terms of the polar angle $\theta$ and azimuthal angle $\phi$. This code outputs the mass flux $F$ along the given direction by specifying $\Delta z$, $\theta$ and $\phi$. More details are available in [OUR PAPER](https://arxiv.org/)


<p align="right">(<a href="#top">back to top</a>)</p>






<!-- ### Built With -->

<!-- This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples. -->





### Prerequisites

* Python 3
* [healpy](https://healpy.readthedocs.io/en/latest/)
* [HEALPix](https://healpix.jpl.nasa.gov/)

### Installation



1. Clone the repo
   ```sh
   git clone https://github.com/tajjankovic/Spin-induced-offset-stream-self-crossing-shocks-in-TDEs.git
   ```
2. Install Python packages
   
<!-- * Instructions for installation on macOS Monterey 12:-->
   ```sh
   pip3 install matplotlib, pandas, healpy

   brew install geos #for Basemap plots

   pip3 install pygeos

   pip3 install basemap #maybe not necessary
   ```
<!-- * Instructions for installation on Ubuntu 20.04:-->
<!-- * Instructions for installation on Windows 10:-->

                
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Basic steps

What does the code do:
* By default it calculates $F$ for $\theta \in [0,\pi]$ and $\phi \in [0,2\pi]$, saves the values to a .txt file and plots a Healpix map of $F$
* Script outflow_parameters.py:
  * Script with paths (for output and input directories) and relevant parameters (for plotting and calculations)
* Script outflow.py:
  * Script for running the code and calculating the normalized mass flux
* Script outflow_plot.py:
  * Script for plotting the data: either a HEALPix map or a Matplotlib contour plot
* User can specify arbitrary values of $\theta$ and $\phi$:
  * Set specific_value = True in the outflow_parameters.py file
  * Change parameters theta_specific, phi_specific in the outflow_parameters.py file
     

### Running the code

* E.g. from the command line for $\Delta z=0.6$ and 1.2:
   ```sh
   python3.8 outflow_final.py --dz_list 0.6 1.2
   ```




   

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP-->

<!-- See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).




<!-- CONTRIBUTING 
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p> -->



<!-- LICENSE 
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p> -->



<!-- CONTACT -->
## Contact

Taj Jankovič - taj.jankovic@ung.si

Project Link: [https://github.com/tajjankovic/Spin-induced-offset-stream-self-crossing-shocks-in-TDEs](https://github.com/tajjankovic/Spin-induced-offset-stream-self-crossing-shocks-in-TDEs)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
<!-- ## References
<a id="1">[1]</a> 
Bonnerot C., Lu W., 2020, Monthly Notices of the Royal Astronomical Society.

<a id="2">[2]</a> 
Bonnerot C., Lu W., 2020, Monthly Notices of the Royal Astronomical Society.

<a id="3">[3]</a> 
Bonnerot C., Lu W., 2020, Monthly Notices of the Royal Astronomical Society.

<a id="4">[4]</a> 
Bonnerot C., Lu W., 2020, Monthly Notices of the Royal Astronomical Society.

<a id="5">[5]</a> 
Bonnerot C., Lu W., 2020, Monthly Notices of the Royal Astronomical Society.

<a id="6">[6]</a> 
Bonnerot C., Lu W., 2020, Monthly Notices of the Royal Astronomical Society.

<a id="7">[7]</a> 
Bonnerot C., Lu W., 2020, Monthly Notices of the Royal Astronomical Society.

<a id="8">[8]</a> 
Bonnerot C., Lu W., 2020, Monthly Notices of the Royal Astronomical Society.

<a id="9">[9]</a> 
Bonnerot C., Lu W., 2020, Monthly Notices of the Royal Astronomical Society.

 -->


<!-- Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet) -->




<!-- MARKDOWN LINKS & IMAGES  -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links 
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge

[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
-->
