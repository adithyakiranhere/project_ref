# Movie Management App - Setup Guide for Windows

Hello! Here’s how to get this MERN stack project up and running on your Windows machine. Follow these steps carefully.

### **Part 1: Prerequisites (Software to Install)**

You need to install these three things first. If you already have them, you can skip to Part 2.

1.  **Node.js (which includes npm):**
    *   Download the "LTS" (Long Term Support) version from the official website: [https://nodejs.org/](https://nodejs.org/)
    *   Run the installer and accept all the default options.
    *   After installation, open a Command Prompt (or PowerShell) and verify it's working by typing:
        ```bash
        node -v
        npm -v
        ```
    *   You should see version numbers for both.

2.  **MongoDB Community Server:**
    *   This is the actual database.
    *   Download the "MSI" installer for Windows from the official site: [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
    *   Run the installer. During the setup, a window will pop up for "MongoDB Compass" (a GUI for the database). It's highly recommended you leave this checked and install it as well.
    *   **Crucially, the installer will set up MongoDB to run automatically as a Windows "Service"**. This means the database will always be running in the background after you restart your PC.

3.  **A Code Editor (Recommended):**
    *   If you don't have one, Visual Studio Code is a great free choice: [https://code.visualstudio.com/](https://code.visualstudio.com/)

---

### **Part 2: Project Setup**

Now that the software is installed, let's set up the project code.

1.  **Open two Command Prompts or PowerShell windows.** You will need one for the backend server and one for the frontend app. It's important to keep them separate.

2.  **Setup the Backend:**
    *   In your **first** command prompt, navigate into the `backend` folder.
        ```bash
        cd path\to\movie-management-app\backend
        ```
    *   Install all the necessary packages by running:
        ```bash
        npm install
        ```
    *   Now, create the environment configuration file. Find the file named `env.example` in this folder, make a copy of it, and rename the copy to `.env`. The default settings in this file should work perfectly with your local MongoDB installation.

3.  **Setup the Frontend:**
    *   In your **second** command prompt, navigate into the `frontend` folder.
        ```bash
        cd path\to\movie-management-app\frontend
        ```
    *   Install all the necessary packages by running:
        ```bash
        npm install
        ```

---

### **Part 3: Running the Application**

With everything set up, let's start the application.

1.  **Start the Backend Server:**
    *   In your **first** command prompt (the one in the `backend` folder), run:
        ```bash
        npm start
        ```
    *   You should see messages like `MongoDB Connected: 127.0.0.1` and `Server running on port 5000`.
    *   **Leave this terminal running!**

2.  **Start the Frontend App:**
    *   In your **second** command prompt (the one in the `frontend` folder), run:
        ```bash
        npm start
        ```
    *   This will automatically open a new tab in your web browser at `http://localhost:3000`.
    *   **Leave this terminal running too!**

You should now see the beautiful Movie Management application in your browser, fully working!

### **Troubleshooting**

*   **Error like `ECONNREFUSED 127.0.0.1:27017` in the backend terminal?**
    *   This means your MongoDB database isn't running. Press `Win + R`, type `services.msc`, and hit Enter. Find "MongoDB Server" in the list and make sure its status is "Running". If not, right-click it and press "Start".
*   **"Network Error" on the website?**
    *   This means your backend server isn't running. Check your first terminal for any errors.
*   **`'node' is not recognized as an internal or external command...`?**
    *   This means Node.js didn't install correctly or you need to restart your computer after installing it.
