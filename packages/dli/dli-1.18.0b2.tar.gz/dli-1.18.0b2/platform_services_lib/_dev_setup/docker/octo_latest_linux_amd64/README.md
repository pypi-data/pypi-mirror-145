# OCTO Command Line Interface

> Represents a CLI tool used to interact with shared services and infrastructure.

## Purpose

This tool acts as an extensibility point to a collection of tools that are packaged independently. Contributors can
extend the CLI with new commands authored in any language as long as they are independently executable.

## Available Commands

The following commands are packaged within this tool:

* **login**: login to cloud platform providers or other systems via SSO
  - **aws**: log into AWS: octo login aws
    - can add --profile parameter to specify a local profile
* **commit**: create a new commit following conventional commits (survey prompt)
* **analyze**: analyze a repository to validate it against a set of rules. The available rules are described in detail
  below.
* **release**: operate on conventional releases
  - **version**: get the next release semantic version based on conventional commits
  - **changelog**: generate a changelog using conventional commits
* **complete**: enable command line completion for BaSH and Zsh
  - **bash**: add completion for bash
  - **zsh**: add completion for zsh

Get more information using the built in help:
```sh
octo [command] --help
```

### Semantic Versioning

The `release` commands will generate [semantic versions][semver-url] automatically utilizing
[conventional commits][conventional-commits-url] to ascertain the type of changes that have occurred between releases.
See [CONTRIBUTING guidelines][commit-guidelines-url] for more information.

At a high level, a version is defined as follows:

[MAJOR].[MINOR].[PATCH]-[BUILD-QUALITY].[BUILD-ITERATION]+[COMMIT-SHA]

The [MAJOR] identifier is incremented if the commit message header contains a breaking change rune (!) after the type
and optional scope. It will also be incremented if the commit message contains the note keywords 'BREAKING CHANGE:'.
The [MINOR] identifier is incremented if the commit message header contains the type `feat`.
The [PATCH] identifier is incremented for all other cases.

In addition, prerelease tags are generated based on the branch name of the the current working tree as follows:

master: not a prerelease
support: not a prerelease

develop: beta.X
release/*: rc.X
hotfix/*: hotfix.X

*: alpha.X

The 'X' variable above is a incremented value based on the number of commits in the current working tree that have been
created since the last release commit.

For instance, assume the following tree on the `develop` branch:

```log
9b64cbb fix: provide short list of regions when user missing perms to full list closes #32
571d498 fix: close browser gracefully by using sigterm and taskkill
bbe4803 fix: close browser gracefully so that cookies saved properly
971e944 (tag: v0.9.3, origin/master) release: v0.9.3 ## v0.9.3 [2019-12-02]
```

In this case, the version that is calculated would be: v0.9.4-beta.3 as there are three (3) commits since the tag
of: v0.9.3. Also of note is that the version will only increment once based on the type of changes that have occurred
until the next release. This is why the version is not v0.9.6-beta.3 as you might otherwise expect.

## Getting Started

This tool has been uploaded to Artifactory (https://repo.ihsmarkit.com and https://repo.mdevlab.com). An account for
either one of these services is required. Please review [confluence][artifactory-confluence-url] for more information.

### Install on Windows

1. [Download][octo-windows-release-url] the archive file from Artifactory
2. Extract the archive
3. Add the octo installation folder to the system path:
    1. Open **Control Panel** -> Search for *Environment* -> click on **Edit the system environment variables**.
    2. Click on **Environment Variables**. Find *Path* in *System Variables*, click on **Edit...**.
    3. Click on **New** and enter the absolute path to the folder containing the octo cli binary and save your changes

### Install on Debian-based Linux

1. Add the repository source (replace \<TOKENS\> for your account and environment):
```sh
sudo sh -c "echo 'deb http://<USER>:<API_KEY>@repo.ihsmarkit.com/artifactory/debian-releases <DISTRIBUTION> main' >> /etc/apt/sources.list"
```
2. Install the package:
```sh
sudo apt install octo
```

### Install on Other *nix Operating Systems (Including macOS)

1. [Download](https://repo.ihsmarkit.com/artifactory/webapp/#/artifacts/browse/tree/General/tar-releases-local/octo/octo-cli) the latest tar.gz for your OS from Artifactory
2. Extract the binary.
3. Install the cli from a shell:
```sh
install octo /usr/local/bin/octo
```

## Extensibility

> NOTE: extensions are currently disabled in distributed versions of the OCTO CLI as this functionality is being
> reworked into the verb-based command line constructs.

This tool acts as an extensibility point to a collection of tools that are packaged independently. Contributors can
extend the CLI with new commands authored in any language as long as they are independently executable. To be eligible
for use as an extension, the following rules apply:

1. The command must be on the users current PATH
2. The command name must begin with "octo-"
3. The command must be packaged as an executable
4. The executable cannot override any of the [existing commands or components](#available-commands).

For example, you can create a bash script as follows:

```sh
# create a folder and add it to the PATH (or use a folder thats already on the PATH) (1)
mkdir ~/example-extension
cd ~/example-extension
export PATH=$PATH:$PWD

# create a bash script -- make sure that it starts with octo- (2)
cat <<EOF > octo-hello
#! /usr/bin/env bash

echo hello world
EOF

# make the script executable (3)
chmod +x octo-hello

# prove that octo detected the extension (4)
octo extensions list

# run the extension with the octo cli
octo hello
```

## Build this Repository

This repository is written in GoLang and has the following prerequisites in order to build the entire toolchain.

* GoLang SDK - used to compile, validate, and test go code.
* goreleaser - used to cross-compile the build for multiple platforms and distributions.
* rpmbuild - used to create RPM packages for RPM-based distributions such as RedHat, CentOS, SUSE, Fedora, etc.

> NOTE: this is NOT required for local development. This is required to build the toolchain within continuous
> integration/delivery scenarios. For local development, please reference the material below.

### Environment Variables

If you're not familiar with GoLang, the following environment variables should be configured:

* **GOBIN**: the path where binaries installed via `go install` are dropped, usually added to the user `PATH`
* **GOPATH**: the path where source and packages are stored when retrieved through a go module or import

### macOS and Linux

The easiest way to get started on macOS or Linux is with [homebrew][homebrew-url]:

```sh
# install go
brew install go

# set the GOPATH and GOBIN when starting a terminal (bashrc)
cat << EOF >> $HOME/.bashrc
export GOPATH=$HOME/.go
export GOBIN=$GOPATH/bin
export PATH=$GOBIN:$PATH
EOF

# start a new terminal to load bashrc (open a new terminal window as an alternative)
exec -l $SHELL
```

### Windows

Please [download][go-download-url] and install the GoLang SDK, which *should* properly configure the toolchain.

### Build and Test Locally

#### Visual Studio Code

1. Install the GoLang extension: `ms-vscode.go`
2. Install the GoLang tools, namely `gopls`
   - NOTE: the language server and go module support is configured within the `.vscode/settings.json` file
   - While the language server is experimental, it is much more stable when working with go modules.
3. Restart the Visual Studio Code Window

Once you have the Go extension enabled and properly configured, you can use the `Go: Build Workspace` and
`Go: Install Current Package` command pallette tasks. to build and install the `main.go`, which will add the executable
to your `$GOBIN` as `octo-cli`, or whatever the name of the folder is that you cloned the repository into. This default
name is a convention of go.

You can also use the CodeLens annotations above unit tests or at the top of test files within any `*_test.go` file to
run tests at the unit, file, or package level.

#### Command Line

Use the following commands to build, test, or install the executable:

```sh
# vet, test, and build the cli on the current platform
./build.sh

# build for all supported platforms and generate archives, including deb and rpm packages
./build.sh --dry-run
```

OR

```powershell
.\build.ps1
```

[artifactory-confluence-url]: https://confluence.ihsmarkit.com/display/DT/Artifactory+-+User+authentication+and+authorization
[go-download-url]: https://golang.org/dl/
[homebrew-url]: https://brew.sh
[octo-windows-release-url]: https://repo.ihsmarkit.com/artifactory/webapp/#/artifacts/browse/tree/General/windows-releases/octo/octo-cli/octo_latest_windows_amd64.zip

[contribute-url]: CONTRIBUTING.md
[commit-guidelines-url]: CONTRIBUTING.md#commit-message-guidelines
[conventional-commits-url]: https://www.conventionalcommits.org
[semver-url]: https://semver.org

Copyright (C) 2019 IHS Markit. See [LICENSE](LICENSE) for details.
