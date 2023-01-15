package ml.cryptovote.auth_service.config;

import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConfigurationProperties("twilio")
public class TwilioConfig {
    @Getter
    @Value("${TWILIO_SID}")
    private String accountSID;
    @Getter
    @Value("${TWILIO_TOKEN}")
    private String authToken;
    @Getter
    @Value("${TWILIO_PHONE}")
    private String phone;

    public TwilioConfig() {
    }
}
