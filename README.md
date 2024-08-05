<a id="readme-top"></a>
<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/TWINSEC3D/simulation">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">TWINSEC3D Simulation: Docker Warehouse Simulation</h3>

  <p align="center">
    An advanced warehouse simulation project using Docker containers and Wazuh SIEM platform.
    <br />
    <a href="https://github.com/TWINSEC3D/simulation"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/TWINSEC3D/simulation">View Demo</a>
    ·
    <a href="https://github.com/TWINSEC3D/simulation/issues">Report Bug</a>
    ·
    <a href="https://github.com/TWINSEC3D/simulation/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

This project provides the source code for a car seat warehouse simulation. It is based on Docker container technology and serves as a cybersecurity testbed using the Wazuh SIEM platform. Each simulation container is individually monitored by a Wazuh agent.

### Built With

* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)
* [Wazuh](https://wazuh.com/)
* [PostgreSQL](https://www.postgresql.org/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Ensure you have Docker and Docker Compose installed on your system.

* Docker
  ```sh
  sudo apt-get install docker-ce docker-ce-cli containerd.io
  ```

* Docker Compose
  ```sh
  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  ```

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/TWINSEC3D/simulation.git
   ```
2. Navigate to the project directory
   ```sh
   cd simulation
   ```
3. Create and configure the `.env` file with your values
   ```env
   INDEXER_URL=https://wazuh.indexer:9200
   INDEXER_USERNAME=admin
   INDEXER_PASSWORD=SecretPassword
   FILEBEAT_SSL_VERIFICATION_MODE=full
   SSL_CERTIFICATE_AUTHORITIES=/etc/ssl/root-ca.pem
   SSL_CERTIFICATE=/etc/ssl/filebeat.pem
   SSL_KEY=/etc/ssl/filebeat.key
   API_USERNAME=wazuh-wui
   API_PASSWORD=MyS3cr37P450r.*-
   OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m
   DASHBOARD_USERNAME=kibanaserver
   DASHBOARD_PASSWORD=kibanaserver
   ```
4. Start the Docker containers
   ```sh
   docker-compose up
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

Use this project as a cybersecurity testbed and to simulate a warehouse environment. Additional examples and screenshots can be added to illustrate how the simulation works and how to interact with it.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Add Changelog
- [ ] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/TWINSEC3D/simulation/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Philip Empl - [philip.empl@ur.de](mailto:philip.empl@ur.de) - University of Regensburg

Project Link: [https://github.com/TWINSEC3D/simulation](https://github.com/TWINSEC3D/simulation)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

## Citation

If you use this project in your research, please cite our paper:

```bibtex
@inproceedings{Glas2024,
  author    = {Magdalena Glas and Johannes Rackl and Philip Empl and Günther Pernul},
  title     = {Asset-Centric OT Security Analytics with Digital Twins},
  booktitle = {9th IEEE European Symposium on Security and Privacy},
  year      = {2024},
  location  = {Vienna, Austria},
  date      = {July 8-12, 2024}
}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/TWINSEC3D/simulation.svg?style=for-the-badge
[contributors-url]: https://github.com/TWINSEC3D/simulation/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TWINSEC3D/simulation.svg?style=for-the-badge
[forks-url]: https://github.com/TWINSEC3D/simulation/network/members
[stars-shield]: https://img.shields.io/github/stars/TWINSEC3D/simulation.svg?style=for-the-badge
[stars-url]: https://github.com/TWINSEC3D/simulation/stargazers
[issues-shield]: https://img

.shields.io/github/issues/TWINSEC3D/simulation.svg?style=for-the-badge
[issues-url]: https://github.com/TWINSEC3D/simulation/issues
[license-shield]: https://img.shields.io/github/license/TWINSEC3D/simulation.svg?style=for-the-badge
[license-url]: https://github.com/TWINSEC3D/simulation/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/your_username
[product-screenshot]: images/screenshot.png

