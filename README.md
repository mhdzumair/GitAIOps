# GitAIOps

![GitAIOps Logo](artifacts/logo.png)

GitAIOps is a ChatGPT plugin that enables ChatGPT to interact with GitLab's CI/CD workflows. It provides a set of API endpoints that allow ChatGPT to execute GitLab API requests.

## Usage

GitAIOps is designed to be used with ChatGPT. Once the plugin is installed, you can ask ChatGPT to perform actions on Git services. Here are some of the things you can do:
- Ability review merge requests
  - provide feedback security.
  - provide feedback code optimization.
  - provide unit test cases.
- Debugging pipeline error (experimental support for scrubbing sensitive data. see [scrub_log function](https://github.com/mhdzumair/GitAIOps/blob/main/utils/log_scrubber.py#L26)).
- Update merge request descriptions.
- And much more! (Basically whatever thing that can do with APIs)

Please note that using this plugin requires a basic understanding of the GitLab and GitHub APIs. Also, be aware that the plugin interacts with data from your Git services, and it's your responsibility to ensure that this data does not contain sensitive information.

## Example Prompt
> - "I have created a merge request [mr link]. Write a code review for it, focusing on best practices such as code maintainability, security vulnerability and performance."
> - "Can you identify the problem in the job link [job link] and provide a detailed explanation of what went wrong and how it can be fixed?"
> - "Please modify the title and description of the merge request based on the modifications made in the merge request located at the following URL: [mr link]"

You can find conversations screenshots in the [example](artifacts/example) folder.


## Supported Git Services

- GitLab
- GitHub
- More to come!


## Local Installation

To install GitAIOps, you need to clone the repository, install the dependencies, and run the server locally. Here are the steps:

1. Make sure you have Python 3.11 installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

2. Clone the GitAIOps repository:

    ```bash
    git clone https://github.com/mhdzumair/GitAIOps.git
    ```

3. Navigate to the GitAIOps directory:

    ```bash
    cd GitAIOps
    ```

4. Install the dependencies using pipenv:

    ```bash
    pipenv install
    ```

5. Run the server:

    ```bash
    pipenv run uvicorn main:app --reload
    ```

Now, you can specify the plugin URL as "localhost:8000" in your ChatGPT settings. 

You also need to store the API tokens for GitLab (`GITLAB_TOKEN`) and GitHub (`GITHUB_TOKEN`) in your environment variables. These tokens allow GitAIOps to authenticate with the Git services and perform actions.


## Security and Compliance

GitAIOps is designed to comply with all applicable laws and OpenAI's usage policies. It does not pose a security vulnerability or threat to users, OpenAI, or any third party. It does not return or contain illegal, defamatory, pornographic, harmful, infringing, or otherwise objectionable content. It does not include any malware, viruses, surveillance, or other malicious programs or code.

## Feedback

If you have any feedback or suggestions on GitAIOps, we would love to hear from you. Please note that if you provide feedback or suggestions, we may freely use that feedback without any obligation to you.

## Legal and License

Please see our [Legal Page](/legal.md) and [License Page](/license.md) for more information.

## Disclaimer

This plugin is currently in development and is not yet available on the ChatGPT plugin store. It is intended for use by developers with permission to run the server locally. Please ensure that you have the necessary permissions before attempting to install and use this plugin.
