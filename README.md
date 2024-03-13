# **CLOUD COMPUTING PROJECT - General Overview**

*Realized by : HADJI Rayan, LATIFI Asmae - TP1 ILC 4A*

[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)

[![Python application](https://github.com/DZburst/4A_ILC_Cloud_Project/actions/workflows/build_app.yml/badge.svg)](https://github.com/DZburst/4A_ILC_Cloud_Project/actions/workflows/build_app.yml)

Our GitHubs : 

<a href="url">[<img src="https://avatars.githubusercontent.com/u/115188188?v=4" align="left" height="70" width="70" style="border-radius: 20%;"><br>HADJI Rayan](https://github.com/DZburst)</a>
<br>
<br>

<a href="url">[<img src="https://avatars.githubusercontent.com/u/116982968?v=4" align="left" height="70" width="70" style="border-radius: 20%;"><br>LATIFI Asmae](https://github.com/Asmlatg)</a>
<br> 
<br> 

---

## Main Steps of the Project

1. Started with the Endpoints, using dictionnaries as in the CI/CD Project
  - Creating all the routes corresponding to the functionnalities in the consigns
  - Taking care of the easiest ones at first, and modifying the others alongside the evolution of the code
  - Testing these endpoints manually and through the front-end when it was possible
2. Replaced the dictionnaries with a key-value database in [Redis](https://redis.io/)
  - Progressive removal of the values linked to the dictionnaries, to replace them with the *redis_client*
  - Keeping the dictionnary while still developping the main functionnalities in case of problem
3. Front-End done progressively with the usual HTML/CSS/JS
4. Tried to solve the [CORS](https://fr.wikipedia.org/wiki/Cross-origin_resource_sharing) errors, without any success ...
5. Started the configuration of the [Docker](https://www.docker.com/) contener, requirements, CIs etc...
6. Added the queue with [RabbitMQ](https://www.rabbitmq.com/)

## Microservice Architecture

<img src="/workspaces/4A_ILC_Cloud_Project/MicroserviceArchitecture.png" alt="Microservice Architecture" style="height: 400px; width:750px;"/>