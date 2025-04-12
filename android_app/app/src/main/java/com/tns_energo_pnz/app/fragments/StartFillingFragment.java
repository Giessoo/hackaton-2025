package com.tns_energo_pnz.app.fragments;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.tns_energo_pnz.app.R;
import com.tns_energo_pnz.app.activities.BaseActivity;

public class StartFillingFragment extends Fragment {
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_start_filling, container, false);
        Button button = view.findViewById(R.id.confirm);
        button.setOnClickListener(v -> ((BaseActivity)getActivity()).switchFragment(new FillingCheckBoxesFragment()));
        return view;
    }
}
