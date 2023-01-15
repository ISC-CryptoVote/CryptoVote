package ml.cryptovote.auth_service.service;

public interface SMSSender {
    void sendSms(String phone, String message);
}
