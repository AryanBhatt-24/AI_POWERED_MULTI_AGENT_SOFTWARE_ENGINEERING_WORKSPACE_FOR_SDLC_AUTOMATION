package com.example.Authify.io;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class ResetPasswordRequest {

    @NotBlank(message = "New Password is required")
    private String newPassword;


     @NotBlank(message = "Otp is required")
    private String otp;

     @NotBlank(message = "Email is Requried")
    private String email;


}
