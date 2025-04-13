package com.tns_energo_pnz.app.controllers;

import java.util.List;
import retrofit2.Call;
import retrofit2.http.GET;

import com.tns_energo_pnz.app.models.User;

public interface UserApi {
    @GET("user")
    Call<List<User>> getUsers();
}