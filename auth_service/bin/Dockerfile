FROM openjdk:11
MAINTAINER crypto-vote.ml
COPY target/auth_service.jar auth_service.jar
COPY config.properties config.properties
ENTRYPOINT ["java","-jar","/auth_service.jar","--spring.config.location=/config.properties,classpath:/application.properties"]