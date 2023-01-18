package ml.cryptovote.auth_service.model.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

import javax.validation.constraints.NotBlank;

@Data
@AllArgsConstructor
public class GsnLoginReqDTO {
    @NotBlank
    private String username;

    @NotBlank
    private String password;

}
