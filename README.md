
Utilities for FireFox Application

  - Usage:
      - to update the firefox Proxy setting quickly on multiple machines.
  - Instructions:
      - XML file is the source for all the Proxy Settings. Update it as per requirement.
      - Update the Python file to look at the XML file for sourcing the proxy settings.
      - Update the batch file to source Python Library then load the python file.
      - Running the Batch file after the above sets should yeild the result.
  
-
CHANGELOG:

   Version 0.1:
-			 -  Initial Release
			 -  Uses XML file to update the Firefox Proxy settings by editing the preferences file.
			 -  Works on WINDOWS Operating System only [Will add MAC,LINUX in future]

  Version 0.2:
-			 -  Updated code to function better
			 -  Used Subprocess to Avoid Firfox Error when not running during terminate.
			 -  Updated to input the File name directly in the Batch File.
			 -  XML file has to be in same folder as python File.
