# Contributing to Inspira

Thank you for your interest in contributing to Inspira! This guide will help you set up your development environment.

## Table of Contents
- [Linux Setup](#linux-setup)
- [Windows Setup](#windows-setup)
- [Alternative IDE Configuration](#alternative-ide-configuration)
- [VS Code Integration](#vs-code-integration)

## Linux Setup

You can use any development environment of your choice. By default, we use **GNOME Builder**.

If you prefer to use **VS Code** or another **IDE**, follow the [Alternative IDE Configuration](#alternative-ide-configuration) section.

### Prerequisites

Make sure you have the following dependencies installed:
- **GTK 4**
- **Libadwaita**
- **Meson**
- **Blueprint Compiler**

Without these dependencies, you may encounter build errors.

---

## Windows Setup

### Prerequisites

First, install the project dependencies using **MSYS2**.

Open PowerShell and install MSYS2:

```powershell
winget install --id=MSYS2.MSYS2 -e
```

Clone the project and navigate to its root directory:

```bash
git clone git@github.com:DaemonWhite/Inspira.git
cd Inspira
```

---

## Alternative IDE Configuration

Three helper scripts are provided in the `tools` directory for use with MSYS2:

```bash
./tools/configure.sh  # Downloads project dependencies
./tools/run.sh        # Compiles and runs the program
./tools/clean.sh      # Cleans the build directory
```

> [!WARNING]
> `./tools/configure.sh` is designed for **Windows with MSYS2**.
> 
> On **Linux**, use this command instead:
> ```sh
> meson setup _build --prefix=$(pwd)/_install
> ```

---

## VS Code Integration

### Setting up MSYS2 Terminal in VS Code

1. Open the project in VS Code
2. Create a `.vscode` folder in the project root
3. Create a `settings.json` file inside `.vscode`

> [!WARNING]
> The paths provided assume you're using the default **MSYS2** installation path.
> 
> On **Linux**, this configuration is unnecessary.

Add the following configuration to enable the MSYS2 shell directly in VS Code:

```json
{
    "terminal.integrated.profiles.windows": {
        "MSYS2_UCRT64": {
            "path": "C:\\msys64\\usr\\bin\\bash.exe",
            "args": [
                "--login",
                "-i"
            ],
            "env": {
                "MSYSTEM": "UCRT64",
                "CHERE_INVOKING": "1"
            }
        }
    },
    "terminal.integrated.defaultProfile.windows": "MSYS2_UCRT64"
}
```

### Creating VS Code Tasks

You can create tasks to run the `tools` scripts directly from VS Code.

Create a `tasks.json` file in the `.vscode` folder:

> [!WARNING]
> The paths provided assume you're using the default **MSYS2** installation path.
> 
> On **Linux**:
> - Replace `args` with `["--login", "-c"]`
> - Replace `executable` with `"/usr/bin/bash"`
> - Replace all `\\` with `/` in paths

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run Inspira",
            "type": "shell",
            "command": "${workspaceFolder}\\tools\\run.sh",
            "options": {
                "shell": {
                    "executable": "C:\\msys64\\usr\\bin\\bash.exe",
                    "args": ["--login", "-i"]
                },
                "env": {
                    "MSYSTEM": "UCRT64",
                    "CHERE_INVOKING": "1"
                }
            },
            "problemMatcher": [],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        },
        {
            "label": "Clean Inspira",
            "type": "shell",
            "command": "${workspaceFolder}\\tools\\clean.sh",
            "options": {
                "shell": {
                    "executable": "C:\\msys64\\usr\\bin\\bash.exe",
                    "args": ["--login", "-i"]
                },
                "env": {
                    "MSYSTEM": "UCRT64",
                    "CHERE_INVOKING": "1"
                }
            },
            "problemMatcher": []
        },
        {
            "label": "Configure Inspira",
            "type": "shell",
            "command": "${workspaceFolder}\\tools\\configure.sh",
            "options": {
                "shell": {
                    "executable": "C:\\msys64\\usr\\bin\\bash.exe",
                    "args": ["--login", "-i"]
                },
                "env": {
                    "MSYSTEM": "UCRT64",
                    "CHERE_INVOKING": "1"
                }
            },
            "problemMatcher": []
        }
    ]
}
```

> [!TIP]
> Congratulations! You've successfully configured VS Code for Inspira development.

---

## Line Endings Configuration

To ensure consistent line endings across different operating systems, configure Git to use LF (Line Feed) for all text files.

Create a `.gitattributes` file in the project root with the following content:

```gitattributes
# Force LF line endings for all text files
* text=auto eol=lf

# Explicitly declare text files
*.sh text eol=lf
*.py text eol=lf
*.md text eol=lf
*.json text eol=lf
*.xml text eol=lf
*.c text eol=lf
*.h text eol=lf

# Denote binary files
*.png binary
*.jpg binary
*.ico binary
```

### For Contributors

If you're contributing to the project, configure your Git to use LF globally:

```bash
git config --global core.autocrlf false
git config --global core.eol lf
```

Or locally for this repository only:

```bash
git config core.autocrlf false
git config core.eol lf
```

> [!NOTE]
> After changing these settings, you may need to refresh your working directory:
> ```bash
> git rm --cached -r .
> git reset --hard
> ```

---

## Getting Help

If you encounter any issues during setup, please:
- Check the [Issues](https://github.com/DaemonWhite/Inspira/issues) page
- Open a new issue with details about your problem
- Include your OS, IDE, and error messages

Happy coding! 🚀