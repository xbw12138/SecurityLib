# SecurityLib
Android Key Security Encryption Native Auto Generation so

## Description
Write the key information into the security.json file in the root directory, execute the generate.py script in the root directory, and automatically generate JNI information, which can be packaged into a jar file. At the same time, the key information will be injected into the so file。

`python generate.py`

`./gradlew assembleDebug`