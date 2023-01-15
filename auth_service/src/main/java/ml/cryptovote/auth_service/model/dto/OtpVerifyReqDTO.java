package ml.cryptovote.auth_service.model.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

@Data
@AllArgsConstructor
public class OtpVerifyReqDTO {
    @NotBlank
    @Pattern(regexp="(\\+94\\d{9})")
    private String phone;

    @NotBlank
    @Pattern(regexp = "(\\d{6})")
    private String otp;
}
