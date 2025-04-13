package com.tns_energo_pnz.app.models;

public class User {
    public int id;
    public String name;
    public String phone;
    public String token;

    @Override
    public String toString() {
        return "User{id=" + id + ", name='" + name + "', phone='" + phone + "', token='[HIDDEN]'}";
    }
}