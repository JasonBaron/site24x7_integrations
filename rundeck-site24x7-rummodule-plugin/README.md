## Rundeck - Site24x7 RUM Module Plugin

Hopefully this is helpful for someone other than just me.

### To use:

##### Update RUM Key and Create Plugin
* Configure RUM for your Rundeck site in Site24x7
* Update RUMKEY in addrummodule.js   
* Zip the Plugin files and copy to rundeck's lib
* Copy the plugin into the libext of your rundeck server
* Restart

```
      pushd ./src/site24x7-rummodule-plugin-1.0.2/resources/js/
      sed -i 's/RUMKEY/[YourRUMKey]/g' addrummodule.js
      popd
      zip -9r site24x7-rummodule-plugin-1.0.2.zip site24x7-rummodule-plugin-1.0.2 META-INF
      cp site24x7-rummodule-plugin-1.0.2.zip [PATH to RUNDECK libext]
     /etc/init.d/rundeckd condrestart
```
Additional resources:

[Rundeck Plugin Development](https://rundeck.org/docs/developer/plugin-development.html)  
[Rundeck UI plugin](https://rundeck.org/docs/developer/ui-plugins.html)  
[Github: Rundeck Plugins](https://github.com/rundeck-plugins)
