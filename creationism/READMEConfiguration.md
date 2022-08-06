## Configuration

This subpackage allows for creating a configuration. A configuration is, in essence, a dictionary with the additional features:

   - configration files, (e.g., yaml, json or any other user defined configuration file) are automatically inserted
   - an addition 'replace' option is available which allows for the replacing dictionary values. standard settings result in the following behavior but can thus be overwritten by a 'replace' tag
     - values that are dictionary are iterativly merged (i.e., not replaced) 
     - values that are list are replaced


#### Examples