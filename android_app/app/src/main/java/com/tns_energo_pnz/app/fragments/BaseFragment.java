package com.tns_energo_pnz.app.fragments;

import android.os.Bundle;

import androidx.fragment.app.Fragment;

public abstract class BaseFragment extends Fragment {

    protected static <T extends BaseFragment> T newInstance(Class<T> fragmentClass, Bundle args) {
        try {
            T fragment = fragmentClass.newInstance();
            fragment.setArguments(args);
            return fragment;
        } catch (Exception e) {
            throw new RuntimeException("Cannot create an instance of " + fragmentClass, e);
        }
    }
}
