## SentinelC App Library

Tooling used to validate, create and publish an app libary feed for the SentinelC platform.

Published applications are importable into a SentinelC cloud controller, browsable in the web app and deployable to appliances using a simple click-through form.

For an example structure of an app libary that uses the tooling provided by this project, see [Demo App Library](https://gitlab.sentinelc.com/sentinel-c/app-library-demo/).

## Specification of an app library structure

### General files hierarchy

- `manifests/`: Contains all apps
  - `app1`: Unique name of the app
    - `app1.yml`: Top-level header. App description
    - `app1-fr.yml`: Optional translation
    - `README.md`: Full description of the app
    - `README-fr.md`: Translated full description
    - `versions/`: List of versions
      - `1.0.0/`: A specific version
        - `app1_1.0.0.kube.yml`: Kubectl with placeholders
        - `app1_1.0.0.yml`: Infos, parameters and architectures
        - `app1_1.0.0-fr.yml`: Translation of ^
      - `1.0.1/`
        - `...`
  - `app2`
    - `...`


### Description file

*{app}.yml in the root of the manifest*

The description file (app1.yml) contains the most basic information about the app. Theses are the following : 

- **display_name**: Application name (translatable)
- **description**: Short description of the app (translatable)
- **homepage**: Official URL of the app.
- **documentation**: Optional URL of the app's documentation.
- **category**: Tag used to categorize the app.
- **deprecated**: True to indicate the app is no longer supported. Defaults to false.

### App README.md

For a full description, a readme can be added and a translation can be provided using a -lang suffix.


### Version file

*{app}_{version}.yml in the versions/ folder*

The version file (app1_1.0.0.yml) contains data specific to the version. There are two top-level keys: `infos` and `vars`.

Basic example:

```yaml
infos:
  architectures:
  - amd64
  - arm64

vars:
  var_key:
    label: Test var
    
ports:
  port_key:
    port: 80
```


#### architectures

List of compatible/supported architectures. Possible values:

- `amd64`
- `arm64`

This indicates that all the images used in the recipe are published to the registry using all the specified architectures.
See https://www.docker.com/blog/multi-arch-build-and-images-the-simple-way/ for more details.

#### Variables

This is used to parameterize the individual instances of the application that will be deployed.

Anything that must or can differ from an instance to another should be defined as a variable.

| Field name  | Type         | Valid values                                            | Default         | Notes                                                        |
| ----------- | ------------ | ------------------------------------------------------- | --------------- | ------------------------------------------------------------ |
| key         | String       | `[a-z_]+`                                               |                 | Name used inside the kube template.                          |
| type        | String       | text, checkbox, number, password, email, url, textarea. | text            | HTML5 input types. Checkbox, number, email and url imply extra validation. |
| label       | Translatable |                                                         | Capitalized key | The field label to display in the user form.                 |
| description | Translatable |                                                         |                 | Help text for the field. Optional                            |
| required    | Boolean      |                                                         | false           | Field cannot be empty. If type is checkbox, it must be checked. |
| regexp      | String       | Python regular expression                               | none            | Value must match the regexp. See django RegexpValidator      |
| default     | String       |                                                         | empty           | A default value. Can be in function(param) format. See supported default functions. |
| auto        | Boolean      |                                                         | false           | Indicates this field is fully auto-generated using the `default` field. |
| secret      | Boolean      |                                                         | false           | Indicates this field is not visible to the user. If auto is false, it is user-provided on creation only, then hidden. If auto is true, it is not visible to the user at all. |
| immutable   | Boolean      |                                                         | false           | The value cannot be changed after creation of the service. This is implied if auto is true. |
| reveal_once | Boolean      |                                                         | false           | Indicates if a secret field should be revealed during the pod creation process. |

*Variable example: Most basic*

```yaml
vars:
  my_var:
```

Gests expanded to:

```yaml
vars:
  my_var:
    type: text
    label: My var
    description: null
    required: false
    regexp: null
    default: ""
    auto: false
    secret: false
    immutable: false
```

*Variable example: A default/initial password that the user can override*

```yaml
vars:
  initial_admin_password:
    description: The initial admin user password you will use to connect to the admin panel after installation.
    required: true
    default: random_hex(12)
    immutable: true
```

*Variable example: A default/initial password that the user can see but not change*

note: immutable is implied to true for all auto field.

```yaml
vars:
  initial_admin_password:
    description: Use this password to login the admin panel for the first time.
    auto: true
    default: random_hex(12)
```

*Variable example: An internal secret that the user does not need to know about*

```yaml
vars:
  mysql_password:
    auto: true
    default: random_hex(32)
    secret: true
```

*Variable example: An initial password that the user can see and override on creation only*

Since `auto` is not set to true, the user will be asked to fill the field even if `secret` is true.

```yaml
vars:
  initial_password:
    default: random_hex(32)
    secret: true
    immutable: true
```

#### Ports

This is used to identify which port to expose.

Ports won't be listed on install if not specified in the recipe.

| Field name   | Type         | Valid values           | Default | Notes                                                        |
| ------------ | ------------ | ---------------------- | ------- | ------------------------------------------------------------ |
| key          | String       | `[a-z_]+`              |         | Name of the functionality linked to the port.                |
| port         | Int          | 80                     |         | Port number                                                  |
| protocol     | String       | "TCP","UDP"            | "TCP"   | Protocol used for communication.                             |
| description  | Translatable |                        |         | Brief description of fonctionality.                          |
| expose_vlan  | String       | "true","false","never" | "false" | Indicate if port is visible to vlan. "never" hides choice on install. |
| expose_cloud | String       | "true","false","never" | "never" | Indicate if port is visible through cloud. "never" hides choice on install. Notes : only http traffic will be forwarded. |

Variable example: Most basic

```yaml
ports:
  app:
    port:80
```

Gests expanded to:

```yaml
ports:
  app:
    port: 80
    protocol: "TCP"
    description: null
    expose_vlan: "false" # Can be changed on install
    expose_cloud: "never" # "never" can't be changed on install
```

### Kube template file

*{app}_{version}.kube.yml in the version folder*

The kube file (app1_1.0.0.kube.yml) contains the yaml description of the pod with placeholders.

The file is in jinja2 template format.


## Using this tool

### Getting the acces token
To create your access token, you need to go to the page https://gitlab.sentinelc.com/-/profile/personal_access_tokens.

You can name it how you want as long as you have the two capabilities

- For docker, you will need : `read_registry`
- For pip, you will need : `read_api`

Write your token down, you wont be able to get it back once generated


### With gitlab-ci in a custom app library

The [demo repository](https://gitlab.sentinelc.com/sentinel-c/app-library-demo) contains a `.gitlab-ci.yml` file with the instructions to publish a feed.
Simply add the script to your own app repository and adds some apps to the `./manifests` folder. 
You might need some to change the builder version if you upgrade your SentinelC instance. 

Once a manifest is created, add the artifact as a repository in the administrative django page.

### Locally using docker

To use our docker image, you must first be logged in using the `docker-login` command.

You will need an access token.

Login with the `docker login -u <username> -p <access_token> gitlab.sentinelc.com:8443`

The username and password are the ones from gitlab.sentinelc.com



You can then pull the image using : `docker run -it -v <working_directory>:/mnt/work gitlab.sentinelc.com:8443/sentinel-c/app-library-builder:<tag> bash`

The working directory is the directory you use to make an app recipe

inside the docker image, use `cd /mnt/work` to access your work directory.

All the tools will be available.

### Locally using a python virtual env

Here are the list of commands to setup your virtual environment

```bash
python3 -m venv env

source env/bin/activate
```

You will need an access token.

To install the tools use this command : `pip install sentinelc-appfeed --extra-index-url https://__token__:<your_personal_token>@gitlab.sentinelc.com/api/v4/projects/113/packages/pypi/simple`

for more information's, you can consult this link: https://gitlab.sentinelc.com/sentinel-c/app-library-builder/-/packages/2

All the tools will be available.

### List of tools :

All tools have a help section by using the -h or --help flag.

Builder :
```bash
  Creates a JSON file containing the valid apps located inside the manifest folder

  how to use
  -------------

  `applib-builder`
  Creates a feed based on the ./manifest folder and output the feed as ./feed/demo-feed.yml

  `applib-builder -p newmanifest -o customfeed -f feed.yml`
  Creates a feed based on the ./newmanifest folder and output the feed as ./customfeed/feed.yml
```

Validator:
```bash
  Validates the folder hiearchy and values of a specific app in the manifest
          
  how to use
  ------------
  `applib-validator newapp`
  Validates the `newapp` app located inside the ./manifests folder
  
  `applib-validator -p newmanifest newapp`
  Validates the `newapp` app located inside the ./newmanifest folder
```

Runner: 
```bash
  Creates a Yaml file that can be 'run with podman using "podman play kube {file}"'

  how to use
  ------------
  `applib-runner newapp 1.0`
  Prompts through all parameters of the app `newapp` app version 1.0 located inside the ./manifest folder
  then create the kubernete config file ./out/newapp{timestamp}

  `applib-runner newapp 1.1 -p newmanifest -o newout -l fr`
  Prompts through all parameters of the `newapp` app version 1.1, using french translations, located inside the ./newmanifest   folder then create the kubernete config file ./newout/newapp{timestamp}
  
  `applib-runner newapp 1.0 -d`
  Creates the kubernete config file ./out/newapp{timestamp} using the default value of each parameter.
```

Recipe: 
```bash
  Create a recipe, either using a template or an older version of the app

  how to use
  ------------
  `applib-recipe newapp 1.0`
  Creates an app called newapp inside the ./manifests folder with a version folder 1.0 that use our app template

  `applib-recipe -p newmanifest newapp 1.0`
  Creates an app called newapp inside the ./newmanifest folder with a version folder 1.0 that use our app template

  `applib-recipe -p newmanifest newapp 1.1 -f 1.0`
  Creates a new version of the app `newapp` inside the ./newmanifest folder with a version folder 1.1 that use the version 1.0 as a base
```



## How to create an app

### First add the template

You can  add the template by using our tools: 

- to create a new app from  scratch use the `applib-recipe {appname} {version}`  command
- to create a new app version use  the `applib-recipe {appname} {new_version} -f  {old_version}`

### Set it as your own

All the  files located in `manifests/{appname}` are description files, you can fill them with the information  found in the [description filed  section](about:blank###Description file).

### Customize the version  file

All the  files located in `manifests/{appname}/versions/version` definitions files. Edit them to get your app  started.

- Add your kubectl with jinja  variables to the `{appname}_{version}.kube.yaml`  file
- Fill the `{appname}_{version}.yaml` file with the  information found in the [version file  section](about:blank###Version file).

### Validate it

Once your  app is set, use the `applib-validator newapp` command to validate your app.

An error  message will be displayed with the information to correct your app if  necessary.

### Create a launchable  test

Once your  app is valid, you can use `applib-runner {appname} {version}` command to create a runnable kube using the files of the  repository.

You can  use the option `-d` to skip  the prompts and use default values.

Once the  command is executed, you will find your executable yaml as `./out/{appname}{timestamp}.yaml`

### Launch your app on a SentinelC  device

To manually test your app on a  sentinelC device before publishing your app, you will need to [connect to it  via ssh](https://sentinelc.com/docs/technical-guides/ssh-connection/) and [create a  zone](https://sentinelc.com/docs/user-guides/dashboard/create-zone).

Write down  your zone id, you will need it later.

Connect to  your device via ssh and copy the generated kube file on it.

Use the  `podman play kube --network network{vlan_id} --mac-address  {random_unused_mac_address} {kubefile}.yaml` command to launch your app. Once launch, use the network ports  to find the IP of your service then add the port-forwarding rules. 

Connect  via the device IP address either by being inside his vlan, connecting via the  vpn or by the proxy.

You can  create new version of your app, upload it and update using `podman play kube --replace  {kubefile}.yaml`

Notes :  You won't have to do any of these steps once the app is  published.

### Publish your app

Add your app to the manifest  folder of [your  repository](about:blank###With gitlab-ci in a custom app library).

Enjoy your  app now as an easily deployable service.

