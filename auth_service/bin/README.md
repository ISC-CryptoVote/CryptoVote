# Auth Service

### Requirements
* java 11 - OpenJDK11 is recommended
* Apache maven - version 3.8.2 is recommended

### Set up the development server
* Clone the git repository
* Open the project in your favourite IDE. (I used IntelliJ IDEA community version https://www.jetbrains.com/idea/download/ )
* Goto `pom.xml` and add missing packages.
* Goto _**Preferences -> Plugins**_, Add **_lombok_** plugin.
* Add config.properties file to the root directory. _(Request it from the backend developer)_
* Add firebase configuration file to /src/main/resources directory. _(Request it from the backend developer)_
* #### Run this command to run the development server
`clean spring-boot:run -Dspring-boot.run.arguments=--spring.config.location=config.properties,classpath:/application.properties -Dspring-boot.run.fork=false`

### Run tests
`./mvnw test`

### Production server
#### To build a jar
`mvn clean package`
#### To run the jar
` java -jar target/ridexapi.jar --spring.config.location=config.properties,classpath:/application.properties`

### API documentation -
* local - http://localhost:8080/swagger-ui.html
* hosted - http://ridex.ml/api/swagger-ui.html
