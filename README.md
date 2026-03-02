# ICHTP - Web-Based Chinese Handwriting Assessment System

**Department of Computer Science**  
**BSCCS Final Year Project 2025-2026**  
**Interim Report I**  
**25CS071**

**Project Title:** Development of a Web-Based Chinese Handwriting Assessment System for Young Children (ICHTP)

**Student Name:** KWOK Ka Chun  
**Student No.:** 58617438  
**Programme Code:** BSCCCU2  
**Supervisor:** Prof LEUNG, Wing Ho Howard  
**Date:** November 10, 2025

---

## Quick Start Guide

### Prerequisites
*   Python 3.8 or higher
*   pip (Python package installer)

### Installation
1.  Open a terminal/command prompt in the project root directory.
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Server
1.  Run the management script to start the Flask server:
    ```bash
    python manage.py run
    ```
2.  The server will start at `http://127.0.0.1:5000`.

### Accessing the Application
*   **Home/Map**: Open your web browser and navigate to `http://127.0.0.1:5000/`.
*   **Authoring Tool**: Access the therapist interface at `http://127.0.0.1:5000/admin/supermarket/authoring`.

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Project Team Organisation](#2-project-team-organisation)
3. [Technical Merits](#3-technical-merits)
4. [Literature Review](#4-literature-review)
5. [Preliminary Design](#5-preliminary-design)
6. [Managerial Process Plan](#6-managerial-process-plan)
7. [Test Plan & Methodology](#7-test-plan--methodology)
8. [Monthly Log](#8-monthly-log)
9. [References](#9-references)

---

## 1. Project Overview

### 1.1 Introduction
Literacy is a key factor in children's development, but for children with dyslexia, this presents a significant obstacle. In Hong Kong, Chinese writing is a significant challenge, particularly for children with dyslexia. In 2008, the Department of Rehabilitation Sciences at the Hong Kong Polytechnic University conducted a pilot study to investigate the effectiveness of the Interactive Computerized Handwriting Training Program (ICHTP). This program, based on the now-defunct Adobe Flash game platform, aimed to improve handwriting skills in Primary 1 students.

The study found that the ICHTP significantly improved children's visual perception and reduced writing time (both time on the page and time spent paused). However, the study also found that this improvement in speed came at the expense of handwriting clarity, with no significant improvement observed in visual-motor integration (VMI) skills. The study concluded that a more structured training program is needed to better develop VMI skills, and recommended modifications to the program to enhance VMI skills. Over a decade later, while the original ICHTP is technically outdated due to the lack of Flash support on the latest Windows platforms, the clinical need it addressed remains, and the initial research effort has paved the way for this project.

This graduation project aims to completely rebuild the ICHTP, building upon the existing system, which has proven clinically effective, and addressing its identified shortcomings. This is not a simple "rebuild," but rather a completely new web-based platform constructed based on modern computer science principles. The project's key technical advantages will be reflected in three key areas: applying programmatic content generation (PCG) technology to create a nearly limitless variety of game challenges; implementing dynamic difficulty adjustment (DDA) technology to create a personalized gamewith experience that adapts to children's real-time performance; and developing a "therapist-in-the-loop" authoring system, allowing therapists to modify portions of the flexible game design within the game to accommodate diverse clinical cases. Therefore, the new platform directly addresses the 2008 study's findings regarding the need for a more systematic and comprehensive ICHTP system.

### 1.2 Purpose, Scope, and Objectives
The primary goal of this project is to design and develop a web-based ICHTP (Interactive Computerized Handwriting Training Program) platform. This project aims to demonstrate that by integrating PCG and DDA technologies, the new ICHTP not only replicates the original ICHTP's effectiveness in improving visual perception and handwriting speed, but also addresses the shortcomings identified in previous studies regarding visual-motor integration and skill retention.

The scope of this project is to develop a client-server web application. The client side will be a browser-based game suite built using the Phaser 3 HTML5 game framework. It will include the development of at least four different game modules, inspired by the original ICHTP's clinical therapeutic games, covering four key areas (visual discrimination, memory sequencing, attention scanning, and motor coordination). Core components of this project include the development of a custom DDA manager to adjust parameters within each game for personalized clinical application, and a Canvas-based PCG engine to generate diverse dynamic game content. The server side will be built using Python Flask to provide a proof-of-concept authoring tool for therapists. The scope of this project does not include a formal clinical trial with patients.

**The main objectives are as follows:**
*   To develop a stable, functional web platform containing at least four unique playable game modules for the game designed in the original ICHTP study.
*   To implement a dynamic decision-making (DDA) system that dynamically adjusts in-game parameters (e.g., time limit, distraction level, number and complexity of questions, etc.) based on available in-game data, such as rolling averages of player accuracy and reaction speed.
*   To build a PCG engine using the HTML5 Canvas API to programmatically generate a variety of graphical assets from source images using various transformations for use in the game.
*   To build a lightweight server-side authoring tool within the game, allowing therapists to upload new graphical assets and modify certain in-game parameters.
*   To establish a client-side data collection framework to record anonymized game data (round completion times, accuracy rates, difficulty adjustment history, etc.) into CSV files, facilitating easier data analysis of the type required for the original 2008 study.

### 1.3 Assumptions, Constraints and Risk
This project relies on a few key assumptions. Firstly, end-users of the games (children and therapists) will engage with a relatively strong desktop web browser (e.g., Chrome, Firefox, Edge) with JavaScript and HTML5 Canvas settings enabled. Therapists using the authoring tool will have basic skills with computer technology; for example, they will be able to upload a file or fill out a form.

**Constraints:**
*   As a final-year project to be completed by a single student, the timeframe for development is limited.
*   The project will use only open-source software and libraries so that licensing can be avoided.
*   The assets used to construct a game (e.g., images and sounds) will favor clarity of a therapeutic activity irrespective of fidelity to an art style.
*   The target population (children with dyslexia) will not be externally involved in the project's assessment of the evaluated games; performance evaluation will be based on the games' technical functionality and feedback from the supervisor and classmates.

**Risks and Mitigation:**
*   **Risk:** The DDA algorithm is poorly tuned, making the activities either frustrating (impossible to challenge) or boring (uninspired).
    *   **Mitigation:** The starting implementation of the DDA algorithm will be a simple but easy-to-debug rule-based model, and the telemetry logs that will be collected will help evaluate, refine, and tune the algorithm in a separate `lab-like' setting. If, due to time, it cannot be tuned, the games will provide all users an option to choose difficulty levels (e.g., Easy, Medium, Hard).
*   **Risk:** The PCG engine generates distractors that are either therapeutically invalid for activities or visually confusing for the children.
    *   **Mitigation:** The PCG engine's configuration file parameters will include (e.g., maximum blur radius, constraints on color saturation, and so on), and I will use a human-in-the-loop tuning process during and between development to come up with reasonably clear constraints for generating distractor challenges that remain distinct and challenging.

### 1.4 Project Deliverables
Upon the projects's completion, the following list of deliveables will be ready.

**Documentation**
*   Project Plan
*   Interim Reports I & II
*   Monthly progress log sheets
*   Final Report of the project
*   Instructions on installing and running the game developed on the list below

**Software**
*   Client-side web application source code (JavaScript, HTML, CSS).
*   The server-side therapist authorizes the tool source code (Python, Flask).
*   Data logs from testing sessions (CSV format).

### 1.5 System Architecture Design
The system's architecture follows the client-server model, with the intention of placing computation-heavy, real-time gameplay on the client and a low-bandwidth server to manage consistently low-resource content.

**Client (Web Browser)**
The client is a Single-Page Application (SPA) and takes control of the complete user experience.
*   **Game Engine (Phaser 3):** This controls the app's lifecycle, including loading the assets, scene transitions (e.g., MainMenuScene, VisualDiscriminationScene), input actions, and rendering to an HTML5 Canvas element.
*   **Procedural Content Generation (PCG) Engine:** This customized JavaScript module utilizes an offscreen HTML5 Canvas. Once a new round of the game starts, the PCG engine takes a source image, processes it through a series of transformations, and draws the final image to the offscreen canvas. This modified image is made available as a texture through Phaser's TextureManager.
*   **Dynamic Difficulty Adjustment (DDA) Manager:** This module maintains a short history of player statistics. After each round, the DDA Manager computes a new scalar of difficulty to be used by the game scene to request appropriately challenging content from the PCG engine.

**Server (Python/Flask)**
The backend server is simple and has two primary services:
*   **Static File Server:** Serves the initial application files (HTML, CSS, and bundled JavaScript) to the user's browser.
*   **RESTful API:** This API exposes some simple HTTP endpoints for the Therapist Authoring Tool (TAT), file management endpoints, and eventually, endpoints to update the configuration.

### 1.6 Methodology
The project's structure will consist of an Iterative and Incremental Model, while a Spiral Model will be used to develop the high-risk components.
The project is appropriate for the iterative model due to the nature of the project as a whole, which will allow for the gradual delivery of functional game modules. The project will start by developing a basic and working prototype, with one game, and then continually add games and capabilities in later iterations.

For the high-risk and innovative components, specifically the PCG and DDA algorithms, an approach based on a Spiral Model is preferable and will work as follows for each cycle:
1.  **Objectives:** Defining specific goals (i.e., "generate a blur effect that is noticeable but not unrecognizable").
2.  **Risk analysis:** Consider the possibilities of failures (ie, the algorithm is too slow; the effect is not therapeutically beneficial)
3.  **Develop:** Build the prototype of the algorithm.
4.  **Evaluate:** Test the prototype against the objectives and plan for the next cycle.

### 1.7 Project Schedule (Milestones)
The project is structured into three phases, aligning with the academic semesters.

| Phase | Period / Objectives | Key Deliverables |
| :--- | :--- | :--- |
| **I** | **(Sep 2025 - Dec 2025) Semester A**<br>Research and foundational prototyping. Establish the core technical foundation and verify the viability of algorithms (PCG and DDA). | **Documentation:** Project Plan, Interim Report I.<br>**Software:** A working prototype of the "Visual Discrimination" game, showcasing the core PCG engine and a basic rule-driven DDA manager, with version-controlled source code available in a private GitHub repository. |
| **II** | **(Jan 2026 - Apr 2026) Semester B**<br>Feature addition and system integration. Create the other three game modules and the server-side therapist authoring tool. | **Documentation:** Interim Report II.<br>**Software:** A fully functional beta version of the platform, with integration of all four game modules and a working prototype of the therapist CMS, capable of uploading assets and adjusting game configurations, along with basic logging of game telemetry. |
| **III** | **(May 2026 - Jul 2026) Summer Term**<br>Testing, polishing, and final reporting: Perform comprehensive testing and debugging, polish the UI/UX experience, and pull together all final documentation. | **Documentation:** Final Report, Presentation slides, Technical Manual.<br>**Software:** The final, stable ICHTP application, a polished version of the CMS, and sample telemetry data, with documentation - all packaged as deliverables. |

---

## 2. Project Team Organisation

### 2.1 External Interfaces
The main external interface will be the project supervisor, Dr. Howard Leung, for academic support and formal assessment.

### 2.2 Internal Structure of Project Team
The project team consists of a single student developer under the direction of an academic supervisor, as follows:
*   **Student Developer:** Kipper, KWOK Ka Chun
*   **Project Supervisor:** Dr. Howard Leung

### 2.3 Roles and Responsibilities
*   **Student Developer:** Responsible for the complete end-to-end development of the project. This covers all research and architectural design, the software development for both client and server testing, and authoring all project documentation required.
*   **Project Supervisor:** Responsible for providing high-level academic guidance, monitoring progress against the project plan, assessing deliverables, and ensuring the project meets a high standard of scholarly and technical rigor.

---

## 3. Technical Merits

### 3.1 Dynamic adjustment of game difficulty as required for children's therapy
The game possesses a continuous level of difficulty which changes after each round by means of two simple signals - the current accuracy, and the average reaction time, in both of which figures an average is taken over a short rolling time, which will avoid figures due to errors caused by unforeseen circumstances and temporary loosening of attention.

The DDA manager computes a rolling accuracy and a median reaction time, with a view to varying the continuous level of difficulty and speed. Suppose the accuracy is high and the reaction is rapid. In that case, the level of difficulty is gradually raised by a small incremental amount to a specific limit, whilst, if the accuracy is low, the level of difficulty is similarly reduced, each increment being mixed in with the previous one to avoid sudden jumps which would be disagreeable to young children.

### 3.2 Hybrid similarity pipeline for safe, controllable challenge
To generate hard-but-fair trials with controllably minor variances, a hybrid similarity score is made which combines some number of fast and aggressive image cues: a small perceptual hash, a gray histogram differencing, a color mean square deviation computed on a downsampled patch, and efficient keypoint matching — if computer vision is provided, and these are combined and normalized to a single score which rises with degree of perceptual similarity.

The pipeline also adapts the acceptance ranges to the current difficulty: as difficulty increases, greater similarity is required of distractors accepted to the answer image, which conveniently narrows the decision boundary about the two images without collapsing it to being equivalent near-duplicates, and low and high pass bands preserve both variety and integrity of the options provided.

The strictest “no-duplicate” guard eliminates candidates that are closely visually similar, and/or closely identical to the answer image, as well as omitting to be contained in the same round similar near-repeats from it to be accepted variants against, to avoid trivial wins, and maintain the value of each of the trials.

### 3.3 Procedural variant generation with runtime evaluation
From any source image supplied by the therapist, the system can make a large number of controlled variants by applying various constrained transformations such as horizontal or vertical flipping, gentle compositing, mild color change in hue and saturation, optional blur, and additional re-scaling to canonical size, the strength and probability of these transformations being proportionate to the ease with which a child may handle the given material in an allowed range.

The similarity pipeline evaluates each generated variant before being introduced into the texture stores of the game; signatures and caches prevent duplications and limit the possibilities, while a small cap of working pool ensures that the time of generation per round is of short duration on the hardware available in the classrooms.

### 3.4 The therapist-in-the-loop authoring and asset management experience
A specialized browser-based authoring interface enables therapists to choose the game and depth of scene and then drag and drop assets that are preprocessed on the client side in a fixed canonical resolution. Oversized assets are automatically compressed with a clear update status, so that uploads are predictable and fast across school networks.

During ingestion, the tool performs lightweight similarity searches into the library to detect potential duplications or near-duplicated items; therapists may accept, override, or delete items with a complete understanding of the reason codes, allowing intentional use of lookalike stimuli when clinically appropriate.

---

## 4. Literature Review

### 4.1 Rationale for design from previous ICHTP data
The original pilot of the Interactive Computerized Handwriting Training Program (ICHTP) conducted on Primary 1 children in Hong Kong examined visual perception and decreased time taken for handwriting completion. Still, a slight improvement in visual-motor integration and handwriting clarity was evident, indicating the need for more structured task design and progression (Poon, 2008). In this current system, the deliberate importance of systematic control of stimuli, graded task difficulty, and transparency of adaptation logic address the recommendation of the study to create a more structured training program that focuses on the development of skills instead of just speed.

### 4.2 Game-based learning principles for engagement and transfer
Game-based environments can facilitate learning by providing challenge, feedback, and identity-safe practice loops that are conducive to persistence and situated understanding, particularly where the mechanics fit the targeted literacy or visuomotor skills (Gee, 2003). For ICHTP, this supports the arguments in favor of using brief trials, immediate feedback on the outcome, and a cumulative structure across sessions to enhance engagement.

### 4.3 Dynamic difficulty adjustment for individualized pacing
Dynamic Difficulty Adjustment (DDA) adjusts the level of challenge in accordance with player performance to prevent prolonged periods of boredom or frustration. It maintains a productive zone of engagement (Hunicke and Chapman, 2004). In pediatric therapy, simple, easily observable variables such as recent accuracy and current reaction time can be used to drive minor but bounded adjustments to exposure time, blank time, and number of selections, etc.

### 4.4 Authoring with the therapist in the loop for clinical fit
Clinical settings often require the customization of content for individual cases, justifying the existence of an authoring layer, wherein therapists can upload images and sounds, curate stimulus libraries, and choose safe ranges for the settings of challenges without changing source code (Yannakakis & Togelius, 2018).

### 4.5 Accessibility and dyslexia-aware presentation
A readable presentation of the task for people with dyslexia stresses clarity of typeface, spacing, colours, and lack of visual clutter, factors which have an effect on accessibility to and performance in the task (Rello & Baeza-Yates, 2016). Recent HCI research into digital reading rulers shows that simple on-screen attention aids can support readers who have tracking and patterning problems, indicating that overlays or screening off that draw attention to present stimuli in therapeutic tasks, be they visual or auditory tasks, can have therapeutic value (Niklaus et al., 2023).

---

## 6. Managerial Process Plan

### 6.1 Project Start-Up Plan
To enable a smooth start, the following initial tasks need to occur:
*   **Version Control Set-Up:** Create a private GitHub repository and design a branching strategy.
*   **Development Environment Set-Up:** Download and configure any software we need, such as Node.js, Python 3, and VS Code.
*   **Initial Literature Review:** Conduct a focused literature review of the PolyU thesis provided to you on ICHTP and more recent papers.

### 6.3 Project Monitoring and Control
*   **Weekly Meetings:** I will schedule a weekly meeting with my supervisor, Dr. Howard Leung.
*   **Progress Logs:** At the end of each month, these logs will be formally compiled.
*   **Version Control:** The Git commit history will document line-by-line, real-time progress.

### 6.4 Risk Management Plan
*   **Assumption Risk:** The primary risk is the assumption that the PCG and DDA algorithms could be successfully integrated. Contingency: substitute a dynamic DDA system for manually set difficulty levels.
*   **Performance Risk:** The real-time canvas generation may be too computationally heavy. Contingency: pre-generation script.
*   **Schedule Slippage:** The semester breaks between phases are purposefully not included and will act as catch-up time.

---

## 7. Test Plan & Methodology
*   **Unit Testing:** PCG Engine, DDA Manager, Similarity Pipeline.
*   **Integration Testing:** Game Scene Loading, DDA + Game Loop, Creation Tools + Server.
*   **System Testing:** Conduct end-to-end play-sessions, Data logging verification, Cross-browser testing.
*   **Usability Testing:** Therapist Interface task-based testing, Game Interface peer-based heuristics.

---

## 9. References
1.  Poon, K. W. (2008). The effect of an interactive computerized handwriting training program to improve Chinese handwriting of children: A pilot study.
2.  Gee, J. P. (2003). What video games have to teach us about learning and literacy.
3.  Hunicke, R., & Chapman, V. (2004). AI for dynamic difficulty adjustment in games.
4.  Yannakakis, G. N., & Togelius, J. (2018). Artificial intelligence and games.
5.  Phaser 3 API Documentation. (n.d.).
6.  Shaywitz, S. E. (2003). Overcoming dyslexia.
7.  Rello, L., & Baeza-Yates, R. (2016). How to present more readable text for people with dyslexia.
8.  Niklaus, A. G., et al. (2023). Digital reading rulers.
