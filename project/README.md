# NASA CMR AI Agent - Project


## CMR Documentation

[CMR Overview](https://www.earthdata.nasa.gov/about/esdis/eosdis/cmr)

[Wiki](https://wiki.earthdata.nasa.gov/display/CMR/Common+Metadata+Repository+Home)

[Wiki - Acronyms](https://wiki.earthdata.nasa.gov/display/CMR/CMR+Client+Partner+User+Guide#CMRClientPartnerUserGuide-Chapter5:Accessingdata)

[Wiki - Request Parameters](https://wiki.earthdata.nasa.gov/display/CMR/CMR+Client+Partner+User+Guide#CMRClientPartnerUserGuide-APIcallsandparametersGETmethod)

[API Documentation](https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html)

### CMR Endpoints

1. autocomplete = Main difference is this allows the q= parameter to be used to search??? and then it returns collections?
2. collections = Descriptions of entire datasets.
3. granules = Descriptions of individual data files within a dataset.

#### Possible Endpoints

I saw somewhere these might be endpoints, but have not tried to access them yet.

- /service
- /tool
- /variable
- /visualizations
- /grid

## TODO LIST

- [ ] Write unit tests for the functions within the "lib" directory.
- [ ] Get agents in working order.
- [ ] Connect the application to the graphio interface instead of using text files.
- [ ] Have some type of CI/CD setup. (*Even if it's not fully fledged for performing evaluations yet*)

## Explanations

- You will notice I have specifically unpacked all of the imports to use `from <MODULE> import`. This was by design to ensure the highest performance without having to import extra items. Upon further research, it seems that this doesn't work in the same way JavaScript does and is generally better to write imports more verbose to make things easier to read.