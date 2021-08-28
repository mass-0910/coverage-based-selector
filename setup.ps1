$CurrentDir = Split-Path $MyInvocation.MyCommand.Path
Set-Location $CurrentDir
mkdir ext-modules
Invoke-WebRequest -Uri https://repo1.maven.org/maven2/junit/junit/4.12/junit-4.12.jar -Outfile ext-modules/junit-4.12.jar
Invoke-WebRequest -Uri https://github.com/EvoSuite/evosuite/releases/download/v1.1.0/evosuite-1.1.0.jar -Outfile ext-modules/evosuite-1.1.0.jar
Invoke-WebRequest -Uri https://github.com/EvoSuite/evosuite/releases/download/v1.1.0/evosuite-standalone-runtime-1.1.0.jar -Outfile ext-modules/evosuite-standalone-runtime-1.1.0.jar
mkdir ext-modules/jacoco
Invoke-WebRequest -Uri https://search.maven.org/remotecontent?filepath=org/jacoco/jacoco/0.8.7/jacoco-0.8.7.zip -Outfile ext-modules/jacoco/jacoco.zip
Expand-Archive -Path ext-modules/jacoco/jacoco.zip -DestinationPath ext-modules/jacoco/