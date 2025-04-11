package com.tns_energo_pnz.app.activities;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;

import com.tns_energo_pnz.app.R;

public class MainActivity extends BaseActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        new Handler().postDelayed(() -> {
            startActivity(new Intent(MainActivity.this, InspectorActivity.class));
            finish();
        }, 3000);
    }

    @Override
    protected int getLayout() {
        return R.layout.activity_main;
    }
}