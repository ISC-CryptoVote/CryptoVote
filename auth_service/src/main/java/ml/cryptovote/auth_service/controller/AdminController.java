package ml.cryptovote.auth_service.controller;

import com.mongodb.DuplicateKeyException;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import ml.cryptovote.auth_service.helper.PasswordGenerator;
import ml.cryptovote.auth_service.model.dao.User;
import ml.cryptovote.auth_service.model.dto.GsnReqDTO;
import ml.cryptovote.auth_service.model.dto.GsnResDTO;
import ml.cryptovote.auth_service.service.UserService;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import javax.validation.Valid;
import java.io.IOException;

@RestController
@RequestMapping("/api/admin")
//@PreAuthorize("hasAuthority('ADMIN')")
@Tag(name = "Admin APIs")
public class AdminController {
    @Autowired
    private UserService userService;

    @Autowired
    ModelMapper modelMapper;

    @PostMapping("/register/gsn")
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "GSN creation")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "201", description = "GSN created successfully"),
            @ApiResponse(responseCode = "400", description = "GSN already exists"),
            @ApiResponse(responseCode = "500", description = "Error in server")
    })
    public GsnResDTO createGSN(@Valid @RequestBody GsnReqDTO data) {
        try {
            String password = PasswordGenerator.generateCommonLangPassword();
            User user = userService.gsnRegistration(data.getUsername(), data.getGnDivision(), password);
            GsnResDTO response = modelMapper.map(user, GsnResDTO.class);
            response.setPassword(password);
            return response;
        } catch (DuplicateKeyException e) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "User already exits");
        }
    }

}
