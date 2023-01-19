package ml.cryptovote.auth_service.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import ml.cryptovote.auth_service.exception.InvalidOperationException;
import ml.cryptovote.auth_service.helper.PasswordGenerator;
import ml.cryptovote.auth_service.model.dto.ChangeVoterStatusReqDTO;
import ml.cryptovote.auth_service.model.dto.VoterVerifiedResDTO;
import ml.cryptovote.auth_service.service.GsnService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/api/gsn")
@PreAuthorize("hasAuthority('GSN')")
public class GsnController {

    @Autowired
    private GsnService gsnService;

    @GetMapping("/voter/pending")
    @ResponseStatus(HttpStatus.OK)
    @Operation(summary = "Get all passengers")
    public List<VoterVerifiedResDTO> getPassengerList() {
        return gsnService.getPendingVoters();
    }

    @PostMapping("/voter/verify")
    @ResponseStatus(HttpStatus.OK)
    @Operation(summary = "GSN creation")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "GSN verify or reject voter"),
            @ApiResponse(responseCode = "400", description = "GSN already exists"),
            @ApiResponse(responseCode = "500", description = "Error in server")
    })
    public VoterVerifiedResDTO verifyVoter(@Valid @RequestBody ChangeVoterStatusReqDTO data) {
        try {
           return gsnService.changeStatus(data.getNic(), data.getStatus());
        } catch (InvalidOperationException e) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, e.getMessage());
        }
    }
}
