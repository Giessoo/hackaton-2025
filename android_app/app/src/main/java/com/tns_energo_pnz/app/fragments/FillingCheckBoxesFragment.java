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

public class FillingCheckBoxesFragment extends Fragment {
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_filling_checkboxes, container, false);
        Button confirm = view.findViewById(R.id.confirm);
        Button back = view.findViewById(R.id.back_button);
        confirm.setOnClickListener(v -> ((BaseActivity)getActivity()).switchFragment(new OverviewFragment()));
        back.setOnClickListener(v -> ((BaseActivity)getActivity()).switchFragment(new StartFillingFragment()));
        return view;
    }
}
