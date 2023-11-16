
# Define ANSI color codes
$Colors = @{
    "RED" = "`e[0;31m"
    "GREEN" = "`e[0;32m"
    "YELLOW" = "`e[0;33m"
    "BLUE" = "`e[0;34m"
    "NC" = "`e[0m" # No Color
}

# Project variables
$PYPI_INDEX = "https://test.pypi.org/legacy/"
$S3_BUCKET_NAME = "ds-ml"
$LOCAL_DATA_DIRECTORY = "./data"
$S3_DATA_PATH = "s3://$S3_BUCKET_NAME/data"

# System detection
$INSTALL_CMD = $null
if ($env:OS -eq "Windows_NT") {
    $INSTALL_CMD = {
        Write-Output "AWS CLI installation not supported directly via this script on Windows. Please install manually."
    }
}
elseif ($env:OS -eq "Unix") {
    $INSTALL_CMD = {
        if ((uname -s) -eq "Linux") {
            Invoke-WebRequest "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -OutFile "awscliv2.zip"
            Expand-Archive "awscliv2.zip" -DestinationPath "."
            sudo ./aws/install
            Remove-Item -Recurse -Force "./aws", "awscliv2.zip"
        }
        elseif ((uname -s) -eq "Darwin") {
            brew install awscli
        }
    }
}

function Install-Poetry {
    # Check if Poetry is already installed
    if (Get-Command 'poetry' -ErrorAction SilentlyContinue) {
        Write-Host "$($Colors.GREEN)Poetry is already installed.$($Colors.NC)"
        return
    }

    # Define the installer script URL
    $installerUrl = "https://install.python-poetry.org"

    # Download and execute the installation script
    try {
        # Use Invoke-Expression to execute the installation command
        (Invoke-WebRequest -UseBasicParsing -Uri $installerUrl).Content | Invoke-Expression
        Write-Host "$($Colors.GREEN)Poetry has been successfully installed.$($Colors.NC)"
    }
    catch {
        Write-Host "$($Colors.RED)An error occurred while installing Poetry$($Colors.NC): $_"
    }

    # Verify the installation
    if (Get-Command 'poetry' -ErrorAction SilentlyContinue) {
        Write-Host "$($Colors.GREEN)Poetry installation verified.$($Colors.NC)"
    } else {
        Write-Host "$($Colors.RED)Poetry installation failed.$($Colors.NC)"
    }
}

function Setup {
    Write-Output "$($Colors.GREEN)Setting up the project using Poetry...$($Colors.NC)"
    poetry install
}

function Activate-Env {
    Write-Output "$($Colors.GREEN)Activating the Poetry virtual environment...$($Colors.NC)"
    poetry shell
}

function Deactivate-Env {
    Write-Output "$($Colors.GREEN)Deactivating the Poetry virtual environment...$($Colors.NC)"
    deactivate
}

function Check-Venv {
    Write-Output "$($Colors.YELLOW)Checking if the Poetry virtual environment is active...$($Colors.NC)"
    poetry env info
}

function Python-Version {
    Write-Output "$($Colors.BLUE)Retrieving Python version used by Poetry...$($Colors.NC)"
    poetry run python --version
}

function Clean {
    Write-Output "$($Colors.RED)Cleaning up Python compiled directories...$($Colors.NC)"
    Get-ChildItem -Recurse -Directory __pycache__, "*.egg-info" | Remove-Item -Recurse -Force
    Get-ChildItem -Recurse -Include *.pyc, *.pyo | Remove-Item -Force
}

function Build {
    Write-Output "$($Colors.GREEN)Building the package...$($Colors.NC)"
    poetry build
}

function Update-Deps {
    Write-Output "$($Colors.YELLOW)Updating project dependencies...$($Colors.NC)"
    poetry update
}

function Jupyter {
    Write-Output "$($Colors.GREEN)Starting Jupyter Notebook...$($Colors.NC)"
    poetry run jupyter notebook
}

function Install-Aws-Cli {
    Write-Output "$($Colors.BLUE)Checking for AWS CLI installation...$($Colors.NC)"
    if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
        Write-Output "$($Colors.GREEN)Installing AWS CLI...$($Colors.NC)"
        & $INSTALL_CMD.Invoke()
    }
}

function Check-Aws-Credentials {
    try {
        aws sts get-caller-identity | Out-Null
        Write-Output "$($Colors.GREEN)AWS credentials found and valid.$($Colors.NC)"
    }
    catch {
        Write-Output "$($Colors.YELLOW)AWS credentials not found or invalid.$($Colors.NC)"
        Write-Output "$($Colors.YELLOW)Please run 'aws configure' to set up your credentials.$($Colors.NC)"
        exit 1
    }
}

function Sync-Data-To-S3 {
    Write-Output "$($Colors.GREEN)Syncing data to the S3 bucket...$($Colors.NC)"
    aws s3 sync $LOCAL_DATA_DIRECTORY $S3_DATA_PATH
}

function Sync-Data-From-S3 {
    Write-Output "$($Colors.GREEN)Syncing data from the S3 bucket...$($Colors.NC)"
    aws s3 sync $S3_DATA_PATH $LOCAL_DATA_DIRECTORY
}

function Pre-Commit {
    Write-Output "$($Colors.YELLO)Running pre-commit hooks...$($Colors.NC)"
    poetry run pre-commit run --all-files
}

function Lint {
    Write-Output "$($Colors.GREEN)Running linters...$($Colors.NC)"
    poetry run flake8 src tests
}

function Format {
    Write-Output "$($Colors.GREEN)Formatting code...$($Colors.NC)"
    poetry run black src tests
}

function Check-Types {
    Write-Output "$($Colors.GREEN)Type-checking with mypy...$($Colors.NC)"
    poetry run mypy src
}

function Code-Quality {
    Write-Output "$($Colors.GREEN)Checking code quality...$($Colors.NC)"
    poetry run flake8 src
    poetry run black src --check
    poetry run mypy src
    # Add any other code quality checks here
}

function Test {
    Write-Output "$($Colors.GREEN)Running tests...$($Colors.NC)"
    poetry run pytest
}

function Test-Coverage {
    Write-Output "$($Colors.GREEN)Running tests with coverage report...$($Colors.NC)"
    poetry run pytest --cov=src
}

function Test-Coverage-Html {
    Write-Output "$($Colors.GREEN)Generating HTML coverage report...$($Colors.NC)"
    poetry run pytest --cov=src --cov-report html
}

function Test-Verbose {
    Write-Output "$($Colors.GREEN)Running tests in verbose mode...$($Colors.NC)"
    poetry run pytest -vv
}

# Show help
function Show-Help {
    foreach ($color in $Colors.GetEnumerator()) {
        Write-Host "$($color.Value)$($color.Key) - $($color.Key) example$($Colors.NC)"
    }
    Write-Output "Available commands:"
    # List the available functions as help, similar to the original Makefile.
}

# Call Show-Help as the default action if no parameters are provided
if ($args.Length -eq 0) {
    Show-Help
}

# Example: powershell .\make.ps1 lint
switch ($args[0]) {
    "setup" { Setup }
    "activate-env" { Activate-Env }
    "deactivate-env" { Deactivate-Env }
    "check-venv" { Check-Venv }
    "python-version" { Python-Version }
    "clean" { Clean }
    "build" { Build }
    # "publish" { Publish } # Commented out as the original Makefile has this commented out.
    "update-deps" { Update-Deps }
    "jupyter" { Jupyter }
    # "data" { Data } # Not implemented as it depends on specifics of your project.
    "install-aws-cli" { Install-Aws-Cli }
    "check-aws-credentials" { Check-Aws-Credentials }
    "sync-data-to-s3" { Sync-Data-To-S3 }
    "sync-data-from-s3" { Sync-Data-From-S3 }
    "lint" { Lint }
    "format" { Format }
    "check-types" { Check-Types }
    "code-quality" { Code-Quality }
    "test" { Test }
    "test-coverage" { Test-Coverage }
    "test-coverage-html" { Test-Coverage-Html }
    "test-verbose" { Test-Verbose }
    "help" { Show-Help }
    Default {
        Write-Host "Command not recognized. Available commands are:"
        Show-Help
    }
}
