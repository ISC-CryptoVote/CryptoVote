package ml.cryptovote.auth_service.model.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import ml.cryptovote.auth_service.enums.Status;

import javax.validation.constraints.NotBlank;

@Data
@AllArgsConstructor
public class ChangeVoterStatusReqDTO {
    @NotBlank
    private String nic;
    @NotBlank
    private Status status;
}
