package ml.cryptovote.auth_service.model.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.RequiredArgsConstructor;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

@Data
@RequiredArgsConstructor
@AllArgsConstructor
public class PhoneAuthReqDTO {
    @NotBlank
    @Pattern(regexp="(\\+94\\d{9})")
    private String phone;
}
