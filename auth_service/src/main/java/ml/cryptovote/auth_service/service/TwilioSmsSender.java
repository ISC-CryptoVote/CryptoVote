package ml.cryptovote.auth_service.service;

import com.twilio.rest.api.v2010.account.Message;
import com.twilio.rest.api.v2010.account.MessageCreator;
import com.twilio.type.PhoneNumber;
import ml.cryptovote.auth_service.config.TwilioConfig;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service("Twilio")
public class TwilioSmsSender implements SMSSender{

    private final TwilioConfig twilioConfig;

    @Autowired
    public TwilioSmsSender(TwilioConfig twilioConfig) {
        this.twilioConfig = twilioConfig;
    }

    @Override
    public void sendSms(String phone, String message) {
        PhoneNumber from = new PhoneNumber(twilioConfig.getPhone());
        PhoneNumber to = new PhoneNumber(phone);
        MessageCreator creator = Message.creator(to, from, message);
        creator.create();
    }
}
