# Workshop Setup Instructions

This guide will walk you through setting up your environment for the workshop.

## 1. Install Python 3.9+

-   **Download**: [https://www.python.org/downloads/](https://www.python.org/downloads/)
-   ⚠️ **Important**: During installation, make sure to check the box that says "Add Python to PATH".
-   **Test**: Open your terminal or command prompt and run `python --version`. You should see a version number like `3.9.x` or higher.

## 2. Install Visual Studio Code

-   **Download**: [https://code.visualstudio.com/](https://code.visualstudio.com/)
-   After installing VS Code, open it and install the official **Python extension** from Microsoft. You can find it in the Extensions view (the icon with squares on the left sidebar).

## 3. Create Workshop Environment

This step creates a dedicated folder for our workshop and a virtual environment to keep our project dependencies isolated.

### For Windows (Command Prompt / PowerShell)

```bash
mkdir mcp-workshop
cd mcp-workshop
python -m venv mcp-env
mcp-env\Scripts\activate
```

### For Mac/Linux (Terminal)

```bash
mkdir mcp-workshop
cd mcp-workshop
python -m venv mcp-env
source mcp-env/bin/activate
```

After running the `activate` command, you should see `(mcp-env)` at the beginning of your terminal prompt. This means the virtual environment is active.

## 4. Install Dependencies

1.  Create a file named `requirements.txt` in your `mcp-workshop` folder.

2.  Add the following content to `requirements.txt`:
    ```
    requests>=2.31.0
    python-dotenv>=1.0.0
    groq>=0.4.1
    # mcp>=1.0.0
    # MCP is commented out for reasons we will explain in class.
    ```

3.  With your `(mcp-env)` active, install these packages by running this command in your terminal:
    ```bash
    pip install -r requirements.txt
    ```

## 5. Get API Key

1.  **Sign up for a free Groq account**: [https://console.groq.com/](https://console.groq.com/)
2.  After signing up, create an API key.
3.  In your `mcp-workshop` folder, create a new file named `.env.local`.
4.  Add the following lines to the `.env.local` file, replacing `your_api_key_here` with the actual API key you got from Groq:
    ```
    GROQ_API_KEY=your_api_key_here
    BASE_API_URL=http://localhost:8000
    ```

## 6. Verify Your Setup

Now, let's make sure everything is working correctly.

### For Windows

Make sure you are in the `mcp-workshop` directory and your `(mcp-env)` is active.
```bash
python -c "import requests, groq; print('✅ Ready!')"
```

### For Mac/Linux

Make sure you are in the `mcp-workshop` directory and your `(mcp-env)` is active.
```bash
python -c "import requests, groq; print('✅ Ready!')"
```

---

## ✅ You're Ready When...

You can run the verification command above and see the message: **✅ Ready!**

## 🆘 Need Help?

Don't worry! If you run into any issues, we can help you out. 