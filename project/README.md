# NASA CMR AI Agent - Project

## TODO LIST

1. Make the ".vscode" directory manually built inside of the devcontainer and use the ".vscode" directory that already exists for computers not using the devcontainer.
2. Get agents in working order.
3. Create shells for rest of project.
4. Have a really simple way for people to just run the project without being in developer mode.
5. Have some type of CI/CD setup. (*Even if it's not fully fledged for performing evaluations yet*)

## CMR NOTES

CMR Overview - <https://www.earthdata.nasa.gov/about/esdis/eosdis/cmr>

Wiki main link - <https://wiki.earthdata.nasa.gov/display/CMR/Common+Metadata+Repository+Home>

Explains the parameters - <https://wiki.earthdata.nasa.gov/display/CMR/CMR+Client+Partner+User+Guide#CMRClientPartnerUserGuide-APIcallsandparametersGETmethod>

Explains the acronyms used - <https://wiki.earthdata.nasa.gov/display/CMR/CMR+Client+Partner+User+Guide#CMRClientPartnerUserGuide-Chapter5:Accessingdata>

<https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html>

Endpoints:

autocomplete = Main difference is this allows the q= parameter to be used to search??? and then it returns collections?
collections = Descriptions of entire datasets.
granules = Descriptions of individual data files within a dataset.

Possible Endpoints:

service ???
tool ???
variable ???
visualizations ???
grid ???

## EXTRA NOTES

You will notice I have specifically unpacked all of the imports to use "from <PACKAGE_NAME> import <Class>/<Function>". This was by design to ensure the highest performance without having to import extra items. (*Might not be necessary, but I think my JavaScript experience rubbed off there.*)