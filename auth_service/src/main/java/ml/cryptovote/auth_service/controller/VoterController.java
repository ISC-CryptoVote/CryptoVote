package ml.cryptovote.auth_service.controller;

import io.swagger.v3.oas.annotations.Operation;
import ml.cryptovote.auth_service.exception.EntityNotFoundException;
import ml.cryptovote.auth_service.exception.InvalidOperationException;
import ml.cryptovote.auth_service.model.dao.Voter;
import ml.cryptovote.auth_service.model.dto.VoterNonceReqDTO;
import ml.cryptovote.auth_service.model.dto.VoterNonceResDTO;
import ml.cryptovote.auth_service.model.dto.VoterNonceVerifyDTO;
import ml.cryptovote.auth_service.service.VoterService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

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
        try {
            return voterService.generateNonce(data.getNic());
        } catch (IllegalArgumentException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "Server Error");
        } catch (EntityNotFoundException e) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, e.getMessage());
        }
    }

    @PostMapping("/nonce/verify")
    @ResponseStatus(HttpStatus.OK)
    @Operation(summary = "Verify public key")
    public Voter verifyNonce(@Valid @RequestBody VoterNonceVerifyDTO data) {
        try {
            return voterService.verifyPubKey(data.getNic(), data.getPubKey(), data.getEncNonce());
        } catch (EntityNotFoundException | InvalidOperationException e) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, e.getMessage());
        } catch (RuntimeException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "Server Error");
        }
    }
}
