# CHANGE LOG

> All notable changes to this project will be documented in this file. See
> [Conventional Commits](https://www.conventionalcommits.org) for commit guidelines.
## v0.10.6 [2020-07-09]

### Patches

* do not modify go mod and sum [53381bcc](53381bcc7997d49dc15e7a518401f6d663252b64)

## v0.10.5 [2020-07-08]

### Bug Fixes

* **commit:** include issue number in commit messages [e1390acb](e1390acbdcd9ecbbc1d6ec80157afcb22f20f00c)

## v0.10.4 [2020-07-07]

### Patches

* make build fully posix complaint [3117571c](3117571cf1facdeaf6035768071395f9f5fc8d40)


## v0.10.2 [2020-07-02]

### Bug Fixes

* **cicd:** removed triggering downstream build [42a7825e](42a7825eb5298f848704e8dbfac90f032946f173)

## v0.10.1 [2020-05-22]

### Bug Fixes

* **release:** fix tests broken by branch env-vars [91be7318](91be731868cd2d06951f1cc2f67ef1f0ee6971ec)
* **release:** detect git branches on detached head [3756e6a6](3756e6a66a4fa8fed978629af1802509115e02f3)

### Patches

* disable staticcheck for now [1ea4c80e](1ea4c80ebb0fd96bd3225b1c3c5eab90bc07b943)
* print the version of go used [462f4cdd](462f4cdd5029f60594d3a322de6d5e162f6443d9)

## v0.10.0-alpha.3 [2020-02-24]

### Features

* **release:** add support for prerelease versions [e24e2d35](e24e2d359a28b078517b41a972431adb70dfe3c2)

### Bug Fixes

* **release:** handle prerelease versions correctly [109177a9](109177a9dce50271b2a00ee8bdc6e2010c3c7405)

## v0.9.9 [2020-01-07]

### Patches

* updated README to show appropriate command for logging into aws [cc519ac6](cc519ac6814cb267d0c9c5da26a4c938645982f3)

## v0.9.8 [2019-12-30]

### Bug Fixes

* login aws display helpful error message if no AWS SSO applications found for user [5212232f](5212232f9effbcb5df0e01ecebd3f8006519e287)

## v0.9.7 [2019-12-19]

### Patches

* fix publish of debian pkg to artifactory [edb5f5ea](edb5f5ea3852505597b5a0ee48304cf5dec1fad7)

## v0.9.6 [2019-12-16]

### Bug Fixes

* provide short list of regions when user missing perms to full list [9b64cbbc](9b64cbbc1aa6a2f2347126bb98e0f2eae898eb51)

## v0.9.5 [2019-12-16]

### Bug Fixes

* close browser gracefully by using sigterm and taskkill [571d4983](571d4983cb8e7a8dcc904cdbf986969ca2277bc1)

## v0.9.4 [2019-12-09]

### Bug Fixes

* close browser gracefully so that cookies saved properly [bbe4803f](bbe4803f09eb085d620556a92997304f08d14b74)

## v0.9.3 [2019-12-02]

### Patches

* **contributing:** add a contributing guide [a3e0bfe7](a3e0bfe73dfa02c5528a8cd14fd1b466f0ba9b15)

## v0.9.2 [2019-11-29]

### Patches

* **readme:** add getting started guide [9c86c595](9c86c595afbcfd9401219971f4504f9ed5bdfcfd)

## v0.9.1 [2019-11-08]

### Bug Fixes

* **login:** removed unnecessary hard-coded azure tenant id [344e930e](344e930eed3f1638b0f50b4de40a36195a2ea8ec)

## v0.9.0 [2019-11-07]

### Features

* add whitesource scanning to octo-cli [40486eb8](40486eb84eb19d68c9f93912d3bb56cac360f23f)
* initial implementation of the octo cli [065b467c](065b467c281903a6c1c0d430cf8e37e0eb4e87b2)
* **analyzers:** add support for repo analyzers [1a1da75c](1a1da75c603fad5bf91743ffb98c4208bff837e7)
* **login:** add parameters for configfile, credentialsfile, and userdatadir [3186412e](3186412e629830d1526d15ad1819c3c7fc19270f)
* **login:** change profile prompt to include default in picklist [4c8ec875](4c8ec875603fd9ff6442d2e5538281e30c33112c)
* **login:** add support to login using a previously saved profile info [067c9cf9](067c9cf9fd080966550e10cc9c9d59e3af5c1594)
* **login:** add support for aws login via active directory [a179aae5](a179aae55a5daf8d1be2e60337495113ece6bdaa)
* **login:** add support for aws login via active directory [e3cc27eb](e3cc27ebeaeb30370ad971aabf47f5be9a4c1314)
* **login:** add aws login via aad sso [65268daa](65268daab423b14be31b10505d2cd795d549d046)
* **login:** add support for session duration [39e1c01b](39e1c01bad1e3fac678214ef9c322cd037a6d974)
* **login:** add support for default output format [938f7ffc](938f7ffc260404c9892dc84190fdb0209aa7f9d7)

### Bug Fixes

* resolve remaining artifactory issues [bffd963c](bffd963c9b21a08c95606991e71b97423e876025)
* ctrl+c at prompt should interrupt process [bebbecee](bebbecee93f4ed5dcd8a101dafe287ae9e58d4a7)
* add account name and role arn to the message when creds saved [8c677c46](8c677c46cf4d1a869e513295cd139506d13282a1)
* include patches in changelog [ef682e98](ef682e986845822c7875c1aef6a430a1175f09e2)
* **login:** added output to list of params loaded from config [889c31c9](889c31c94b1fef6c23ad2c265ab2ea27faf1f0f8)
* **release:** use correct dates for changelog [95b62336](95b62336b97df1a1c6dde56f9e78167cee910d5b)

### Patches

* rename darwin to macos [4c35e8a6](4c35e8a6e69c2e92ecee743b4759bac67800a9f9)
* add tap for homebrew macos and linux [6381294a](6381294a8b3201d419e49b05abea3c0378d1a0b8)
* simplify the build pipeline [ab49ef91](ab49ef91c45d6e253ae994da036c0173e33c5f18)
* attempt to resolve gitlab pipeline one more time [3546d963](3546d96312184c0e13cfb3ebe8178e16fc4f14cd)
* fix gitlab weirdness [12e86e58](12e86e5824d688869b75b6687ef7b13236cdbcf7)
* fix build-id environment variable [13ae5a79](13ae5a7901b4785d7ecb09e2eb5f66a562aa6442)
* move commit before goreleaser [45745319](45745319a064bd12bf491e7b978c40abbc8d69ac)
* resolve issue with go module changes [749a0bb3](749a0bb318b63856f53e7d77d53c7bbf771a555a)
* fix release commit push option [e8e513f7](e8e513f77a33cd2a1cf304207d630eb9bb54b1fc)
* improve build system and artifactory push [3082187b](3082187b4d8f895c58ec2cb5c848967b1ea5eb61)
* switch to goreleaser for build [de2e3f52](de2e3f5239001f196744fe789503674e98965251)
* move push back to build phase [b7b608f3](b7b608f35adf3fc373df38f96c04141c87a6e572)
* Need drop down selector for region [e6c30376](e6c30376ea2b6705b4ad1c1ed97a5f302eadc6c7)
* use git add force for ignored files [136c34ee](136c34eee55fcd00b103255c10a49d5b1c80d200)
* only push release commit on success [9f6c737c](9f6c737c12b800fab41910f2759825f4417f77a4)
* add push for artifactory assets [9f0c6c89](9f0c6c89e39bdec2abbe7385f6b8cc6b76d7622c)
* test environment variables [64477896](644778963a9f3ac71865cf28c7c47d93b2445005)
* allow empty release commit [309eff65](309eff6564e0737a25f467ab380fe40f2ef768ea)
* fix goreleaser url templates [8d812f1c](8d812f1c90793695ea4f0310f3b4051e412e1cd6)
* **build:** fix metadata flags [252a0f59](252a0f590a33cd957c410e85b5f164a626af2fe0)
* **build:** remove test-race from default targets [3d794142](3d7941429538eedd680b6bfebfb9b2ad0a793e66)
* **login:** create credentials and config file if none exists [ecc9384c](ecc9384c6c5c0ad384221dc7e232cfe2eaf24c9b)
* **login:** Use pointer to options instead of args [b6dc6bbf](b6dc6bbf3604e61b8bb0130f554182ba631cecba)
* **login:** fixed bug in saving default file to credentials and config [de299b80](de299b80c410527120ab5be6ce077828c6a43a24)
* **readme:** update readme with latest build changes [e61afc88](e61afc8804953e169edf125075002edf6644fb29)

## v0.8.0 [2019-11-07]

### Features

* add whitesource scanning to octo-cli [40486eb8](40486eb84eb19d68c9f93912d3bb56cac360f23f)
* initial implementation of the octo cli [065b467c](065b467c281903a6c1c0d430cf8e37e0eb4e87b2)
* **analyzers:** add support for repo analyzers [1a1da75c](1a1da75c603fad5bf91743ffb98c4208bff837e7)
* **login:** add parameters for configfile, credentialsfile, and userdatadir [3186412e](3186412e629830d1526d15ad1819c3c7fc19270f)
* **login:** change profile prompt to include default in picklist [4c8ec875](4c8ec875603fd9ff6442d2e5538281e30c33112c)
* **login:** add support to login using a previously saved profile info [067c9cf9](067c9cf9fd080966550e10cc9c9d59e3af5c1594)
* **login:** add support for aws login via active directory [a179aae5](a179aae55a5daf8d1be2e60337495113ece6bdaa)
* **login:** add support for aws login via active directory [e3cc27eb](e3cc27ebeaeb30370ad971aabf47f5be9a4c1314)
* **login:** add aws login via aad sso [65268daa](65268daab423b14be31b10505d2cd795d549d046)
* **login:** add support for session duration [39e1c01b](39e1c01bad1e3fac678214ef9c322cd037a6d974)
* **login:** add support for default output format [938f7ffc](938f7ffc260404c9892dc84190fdb0209aa7f9d7)

### Bug Fixes

* resolve remaining artifactory issues [bffd963c](bffd963c9b21a08c95606991e71b97423e876025)
* ctrl+c at prompt should interrupt process [bebbecee](bebbecee93f4ed5dcd8a101dafe287ae9e58d4a7)
* add account name and role arn to the message when creds saved [8c677c46](8c677c46cf4d1a869e513295cd139506d13282a1)
* include patches in changelog [ef682e98](ef682e986845822c7875c1aef6a430a1175f09e2)
* **login:** added output to list of params loaded from config [889c31c9](889c31c94b1fef6c23ad2c265ab2ea27faf1f0f8)
* **release:** use correct dates for changelog [95b62336](95b62336b97df1a1c6dde56f9e78167cee910d5b)

### Patches

* rename darwin to macos [4c35e8a6](4c35e8a6e69c2e92ecee743b4759bac67800a9f9)
* add tap for homebrew macos and linux [6381294a](6381294a8b3201d419e49b05abea3c0378d1a0b8)
* simplify the build pipeline [ab49ef91](ab49ef91c45d6e253ae994da036c0173e33c5f18)
* attempt to resolve gitlab pipeline one more time [3546d963](3546d96312184c0e13cfb3ebe8178e16fc4f14cd)
* fix gitlab weirdness [12e86e58](12e86e5824d688869b75b6687ef7b13236cdbcf7)
* fix build-id environment variable [13ae5a79](13ae5a7901b4785d7ecb09e2eb5f66a562aa6442)
* move commit before goreleaser [45745319](45745319a064bd12bf491e7b978c40abbc8d69ac)
* resolve issue with go module changes [749a0bb3](749a0bb318b63856f53e7d77d53c7bbf771a555a)
* fix release commit push option [e8e513f7](e8e513f77a33cd2a1cf304207d630eb9bb54b1fc)
* improve build system and artifactory push [3082187b](3082187b4d8f895c58ec2cb5c848967b1ea5eb61)
* switch to goreleaser for build [de2e3f52](de2e3f5239001f196744fe789503674e98965251)
* move push back to build phase [b7b608f3](b7b608f35adf3fc373df38f96c04141c87a6e572)
* Need drop down selector for region [e6c30376](e6c30376ea2b6705b4ad1c1ed97a5f302eadc6c7)
* use git add force for ignored files [136c34ee](136c34eee55fcd00b103255c10a49d5b1c80d200)
* only push release commit on success [9f6c737c](9f6c737c12b800fab41910f2759825f4417f77a4)
* add push for artifactory assets [9f0c6c89](9f0c6c89e39bdec2abbe7385f6b8cc6b76d7622c)
* test environment variables [64477896](644778963a9f3ac71865cf28c7c47d93b2445005)
* allow empty release commit [309eff65](309eff6564e0737a25f467ab380fe40f2ef768ea)
* fix goreleaser url templates [8d812f1c](8d812f1c90793695ea4f0310f3b4051e412e1cd6)
* **build:** fix metadata flags [252a0f59](252a0f590a33cd957c410e85b5f164a626af2fe0)
* **build:** remove test-race from default targets [3d794142](3d7941429538eedd680b6bfebfb9b2ad0a793e66)
* **login:** create credentials and config file if none exists [ecc9384c](ecc9384c6c5c0ad384221dc7e232cfe2eaf24c9b)
* **login:** Use pointer to options instead of args [b6dc6bbf](b6dc6bbf3604e61b8bb0130f554182ba631cecba)
* **login:** fixed bug in saving default file to credentials and config [de299b80](de299b80c410527120ab5be6ce077828c6a43a24)
* **readme:** update readme with latest build changes [e61afc88](e61afc8804953e169edf125075002edf6644fb29)

## v0.7.0 [2019-11-07]

### Features

* add whitesource scanning to octo-cli [40486eb8](40486eb84eb19d68c9f93912d3bb56cac360f23f)
* initial implementation of the octo cli [065b467c](065b467c281903a6c1c0d430cf8e37e0eb4e87b2)
* **analyzers:** add support for repo analyzers [1a1da75c](1a1da75c603fad5bf91743ffb98c4208bff837e7)
* **login:** add parameters for configfile, credentialsfile, and userdatadir [3186412e](3186412e629830d1526d15ad1819c3c7fc19270f)
* **login:** change profile prompt to include default in picklist [4c8ec875](4c8ec875603fd9ff6442d2e5538281e30c33112c)
* **login:** add support to login using a previously saved profile info [067c9cf9](067c9cf9fd080966550e10cc9c9d59e3af5c1594)
* **login:** add support for aws login via active directory [a179aae5](a179aae55a5daf8d1be2e60337495113ece6bdaa)
* **login:** add support for aws login via active directory [e3cc27eb](e3cc27ebeaeb30370ad971aabf47f5be9a4c1314)
* **login:** add aws login via aad sso [65268daa](65268daab423b14be31b10505d2cd795d549d046)
* **login:** add support for session duration [39e1c01b](39e1c01bad1e3fac678214ef9c322cd037a6d974)
* **login:** add support for default output format [938f7ffc](938f7ffc260404c9892dc84190fdb0209aa7f9d7)

### Bug Fixes

* resolve remaining artifactory issues [bffd963c](bffd963c9b21a08c95606991e71b97423e876025)
* ctrl+c at prompt should interrupt process [bebbecee](bebbecee93f4ed5dcd8a101dafe287ae9e58d4a7)
* add account name and role arn to the message when creds saved [8c677c46](8c677c46cf4d1a869e513295cd139506d13282a1)
* include patches in changelog [ef682e98](ef682e986845822c7875c1aef6a430a1175f09e2)
* **login:** added output to list of params loaded from config [889c31c9](889c31c94b1fef6c23ad2c265ab2ea27faf1f0f8)
* **release:** use correct dates for changelog [95b62336](95b62336b97df1a1c6dde56f9e78167cee910d5b)

### Patches

* rename darwin to macos [4c35e8a6](4c35e8a6e69c2e92ecee743b4759bac67800a9f9)
* add tap for homebrew macos and linux [6381294a](6381294a8b3201d419e49b05abea3c0378d1a0b8)
* simplify the build pipeline [ab49ef91](ab49ef91c45d6e253ae994da036c0173e33c5f18)
* attempt to resolve gitlab pipeline one more time [3546d963](3546d96312184c0e13cfb3ebe8178e16fc4f14cd)
* fix gitlab weirdness [12e86e58](12e86e5824d688869b75b6687ef7b13236cdbcf7)
* fix build-id environment variable [13ae5a79](13ae5a7901b4785d7ecb09e2eb5f66a562aa6442)
* move commit before goreleaser [45745319](45745319a064bd12bf491e7b978c40abbc8d69ac)
* resolve issue with go module changes [749a0bb3](749a0bb318b63856f53e7d77d53c7bbf771a555a)
* fix release commit push option [e8e513f7](e8e513f77a33cd2a1cf304207d630eb9bb54b1fc)
* improve build system and artifactory push [3082187b](3082187b4d8f895c58ec2cb5c848967b1ea5eb61)
* switch to goreleaser for build [de2e3f52](de2e3f5239001f196744fe789503674e98965251)
* move push back to build phase [b7b608f3](b7b608f35adf3fc373df38f96c04141c87a6e572)
* Need drop down selector for region [e6c30376](e6c30376ea2b6705b4ad1c1ed97a5f302eadc6c7)
* use git add force for ignored files [136c34ee](136c34eee55fcd00b103255c10a49d5b1c80d200)
* only push release commit on success [9f6c737c](9f6c737c12b800fab41910f2759825f4417f77a4)
* add push for artifactory assets [9f0c6c89](9f0c6c89e39bdec2abbe7385f6b8cc6b76d7622c)
* test environment variables [64477896](644778963a9f3ac71865cf28c7c47d93b2445005)
* allow empty release commit [309eff65](309eff6564e0737a25f467ab380fe40f2ef768ea)
* fix goreleaser url templates [8d812f1c](8d812f1c90793695ea4f0310f3b4051e412e1cd6)
* **build:** fix metadata flags [252a0f59](252a0f590a33cd957c410e85b5f164a626af2fe0)
* **build:** remove test-race from default targets [3d794142](3d7941429538eedd680b6bfebfb9b2ad0a793e66)
* **login:** create credentials and config file if none exists [ecc9384c](ecc9384c6c5c0ad384221dc7e232cfe2eaf24c9b)
* **login:** Use pointer to options instead of args [b6dc6bbf](b6dc6bbf3604e61b8bb0130f554182ba631cecba)
* **login:** fixed bug in saving default file to credentials and config [de299b80](de299b80c410527120ab5be6ce077828c6a43a24)
* **readme:** update readme with latest build changes [e61afc88](e61afc8804953e169edf125075002edf6644fb29)

## v0.6.4 [2019-11-07]

### Patches

* fix goreleaser url templates [8d812f1c](8d812f1c90793695ea4f0310f3b4051e412e1cd6)

## v0.6.3 [2019-11-07]

### Bug Fixes

* resolve remaining artifactory issues [bffd963c](bffd963c9b21a08c95606991e71b97423e876025)

## v0.6.2 [2019-11-06]

### Bug Fixes

* ctrl+c at prompt should interrupt process [bebbecee](bebbecee93f4ed5dcd8a101dafe287ae9e58d4a7)

## v0.6.1 [2019-11-05]

### Bug Fixes

* add account name and role arn to the message when creds saved [8c677c46](8c677c46cf4d1a869e513295cd139506d13282a1)

## v0.6.0 [2019-11-04]

### Features

* add whitesource scanning to octo-cli [40486eb8](40486eb84eb19d68c9f93912d3bb56cac360f23f)

## v0.5.1 [2019-11-04]

### Bug Fixes

* **release:** use correct dates for changelog [95b62336](95b62336b97df1a1c6dde56f9e78167cee910d5b)

## v0.5.0 [2019-10-21]

### Features

* **login:** add parameters for configfile, credentialsfile, and userdatadir [3186412e](3186412e629830d1526d15ad1819c3c7fc19270f)

## v0.4.0 [2019-10-17]

### Features

* **login:** change profile prompt to include default in picklist [4c8ec875](4c8ec875603fd9ff6442d2e5538281e30c33112c)

## v0.3.9 [2019-10-07]

### Patches

* add tap for homebrew macos and linux [6381294a](6381294a8b3201d419e49b05abea3c0378d1a0b8)

## v0.3.8 [2019-10-07]

### Patches

* simplify the build pipeline [ab49ef91](ab49ef91c45d6e253ae994da036c0173e33c5f18)

## v0.3.7 [2019-10-07]

### Patches

* attempt to resolve gitlab pipeline one more time [3546d963](3546d96312184c0e13cfb3ebe8178e16fc4f14cd)
* fix gitlab weirdness [12e86e58](12e86e5824d688869b75b6687ef7b13236cdbcf7)

## v0.3.6 [2019-10-07]

### Patches

* fix build-id environment variable [13ae5a79](13ae5a7901b4785d7ecb09e2eb5f66a562aa6442)

## v0.3.5 [2019-10-07]

### Patches

* move commit before goreleaser [45745319](45745319a064bd12bf491e7b978c40abbc8d69ac)
* resolve issue with go module changes [749a0bb3](749a0bb318b63856f53e7d77d53c7bbf771a555a)

## v0.3.4 [2019-10-04]

### Patches

* fix release commit push option [e8e513f7](e8e513f77a33cd2a1cf304207d630eb9bb54b1fc)

## v0.3.3 [2019-10-04]

### Patches

* improve build system and artifactory push [3082187b](3082187b4d8f895c58ec2cb5c848967b1ea5eb61)

## v0.3.2 [2019-10-04]

### Patches

* **login:** Use pointer to options instead of args [b6dc6bbf](b6dc6bbf3604e61b8bb0130f554182ba631cecba)

## v0.3.1 [2019-10-01]

### Patches

* move push back to build phase [b7b608f3](b7b608f35adf3fc373df38f96c04141c87a6e572)
* Need drop down selector for region [e6c30376](e6c30376ea2b6705b4ad1c1ed97a5f302eadc6c7)
* use git add force for ignored files [136c34ee](136c34eee55fcd00b103255c10a49d5b1c80d200)
* only push release commit on success [9f6c737c](9f6c737c12b800fab41910f2759825f4417f77a4)

## v0.3.0 [2019-10-01]

### Features

* **login:** add support for session duration [39e1c01b](39e1c01bad1e3fac678214ef9c322cd037a6d974)

## v0.2.4 [2019-09-30]

### Patches

* add push for artifactory assets [9f0c6c89](9f0c6c89e39bdec2abbe7385f6b8cc6b76d7622c)

## v0.2.3 [2019-09-30]

### Bug Fixes

* **login:** added output to list of params loaded from config [889c31c9](889c31c94b1fef6c23ad2c265ab2ea27faf1f0f8)

## v0.2.2 [2019-09-30]

### Patches

* **readme:** update readme with latest build changes [e61afc88](e61afc8804953e169edf125075002edf6644fb29)

## v0.2.1 [2019-09-29]

### Patches

* **login:** create credentials and config file if none exists [ecc9384c](ecc9384c6c5c0ad384221dc7e232cfe2eaf24c9b)

## v0.2.0 [2019-09-29]

### Features

* **login:** add support for default output format [938f7ffc](938f7ffc260404c9892dc84190fdb0209aa7f9d7)

## v0.1.2 [2019-09-26]

### Bug Fixes

* include patches in changelog [ef682e98](ef682e986845822c7875c1aef6a430a1175f09e2)

## v0.1.1 [2019-09-26]

### Patches

* rename darwin to macos [4c35e8a6](4c35e8a6e69c2e92ecee743b4759bac67800a9f9)

## v0.1.0 [2019-09-26]

### Features

* initial implementation of the octo cli [065b467c](065b467c281903a6c1c0d430cf8e37e0eb4e87b2)
* **analyzers:** add support for repo analyzers [1a1da75c](1a1da75c603fad5bf91743ffb98c4208bff837e7)
* **login:** add support to login using a previously saved profile info [067c9cf9](067c9cf9fd080966550e10cc9c9d59e3af5c1594)
* **login:** add support for aws login via active directory [a179aae5](a179aae55a5daf8d1be2e60337495113ece6bdaa)
* **login:** add support for aws login via active directory [e3cc27eb](e3cc27ebeaeb30370ad971aabf47f5be9a4c1314)
* **login:** add aws login via aad sso [65268daa](65268daab423b14be31b10505d2cd795d549d046)

### Patches

* allow empty release commit [309eff65](309eff6564e0737a25f467ab380fe40f2ef768ea)
* test environment variables [64477896](644778963a9f3ac71865cf28c7c47d93b2445005)
* switch to goreleaser for build [de2e3f52](de2e3f5239001f196744fe789503674e98965251)
* **build:** fix metadata flags [252a0f59](252a0f590a33cd957c410e85b5f164a626af2fe0)
* **build:** remove test-race from default targets [3d794142](3d7941429538eedd680b6bfebfb9b2ad0a793e66)
* **login:** fixed bug in saving default file to credentials and config [de299b80](de299b80c410527120ab5be6ce077828c6a43a24)
