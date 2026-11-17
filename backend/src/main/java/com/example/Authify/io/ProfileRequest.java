package com.example.Authify.io;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class ProfileRequest {

    @NotBlank(message = " Name should not be empty")
    private String name;

    @Email(message = "Enter the valid email")
    @NotNull(message = "Email should Not be Empty")
    private String email;

    @Size(min=6 , message="password must be alteast 6 digit number")
    private String password;


}