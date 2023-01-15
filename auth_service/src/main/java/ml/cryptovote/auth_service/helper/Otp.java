package ml.cryptovote.auth_service.helper;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class Otp {
    private final String otp;
    private final long exp;
}
