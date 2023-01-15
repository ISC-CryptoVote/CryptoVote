package ml.cryptovote.auth_service.controller;

import com.mongodb.DuplicateKeyException;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import ml.cryptovote.auth_service.enums.Role;
import ml.cryptovote.auth_service.model.dto.MessageDTO;
import ml.cryptovote.auth_service.model.dto.PhoneAuthReqDTO;
import ml.cryptovote.auth_service.model.dto.OtpVerifyReqDTO;
import ml.cryptovote.auth_service.model.dto.VoterVerifiedResDTO;
import ml.cryptovote.auth_service.service.UserService;
import ml.cryptovote.auth_service.exception.InvalidOperationException;
import ml.cryptovote.auth_service.exception.EntityNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.AuthenticationException;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.server.ResponseStatusException;

import javax.validation.Valid;
import java.security.InvalidKeyException;

@RestController
@RequestMapping("/api/auth")
@Tag(name = "Auth APIs")
public class AuthController {
    @Autowired
    private UserService userService;

    @Autowired
    private AuthenticationManager authenticationManager;

    @PostMapping("/voter/phoneAuth")
    @ResponseStatus(HttpStatus.OK)
    @Operation(summary = "Send OTP/voter")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Saved user in memory"),
            @ApiResponse(responseCode = "500", description = "Unable to generate OTP")
    })
    public MessageDTO voterPhoneAuth(@Valid @RequestBody PhoneAuthReqDTO data) {
        try {

            return new MessageDTO(userService.sendOTP(data.getPhone(), Role.VOTER));
        } catch (InvalidKeyException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, e.getMessage());
        }
    }

    @PostMapping("/voter/phoneVerify")
    @ResponseStatus(HttpStatus.OK)
    @Operation(summary = "Verify OTP/voter")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Login/Signup"),
            @ApiResponse(responseCode = "401", description = "Invalid OTP/phone"),
            @ApiResponse(responseCode = "403", description = "User is suspended")
    })
    public VoterVerifiedResDTO voterPhoneVerify(@Valid @RequestBody OtpVerifyReqDTO data) {
        try{
            VoterVerifiedResDTO response = userService.voterVerification(data.getPhone(), data.getOtp());
            authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(data.getPhone(),response.getRefreshToken()));
            return response;
        }
        catch (InvalidOperationException | EntityNotFoundException | AuthenticationException e) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, e.getMessage());
        } catch (DuplicateKeyException e) {
            throw new ResponseStatusException(HttpStatus.FORBIDDEN, "User is suspended");
        }
    }
}
