package ml.cryptovote.auth_service.controller;

import io.swagger.v3.oas.annotations.Operation;
import ml.cryptovote.auth_service.model.dto.VoterNonceReqDTO;
import ml.cryptovote.auth_service.model.dto.VoterNonceResDTO;
import ml.cryptovote.auth_service.service.VoterService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;

@RestController
@RequestMapping("/api/voter")
public class VoterController {

    @Autowired
    private VoterService voterService;

    @PostMapping("/nonce")
    @ResponseStatus(HttpStatus.OK)
    @Operation(summary = "Get nonce")
    public VoterNonceResDTO requestNonce(@Valid @RequestBody VoterNonceReqDTO data) {
        return voterService.generateNonce(data.getNic());
    }
}
