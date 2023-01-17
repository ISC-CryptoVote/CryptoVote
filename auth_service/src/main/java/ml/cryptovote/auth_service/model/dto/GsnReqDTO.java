package ml.cryptovote.auth_service.model.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class GsnReqDTO {
    private String username;
    private String gnDivision;
}
