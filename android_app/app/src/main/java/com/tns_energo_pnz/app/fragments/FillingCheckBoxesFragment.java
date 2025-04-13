package com.tns_energo_pnz.app.fragments;

import static android.app.Activity.RESULT_OK;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.text.format.DateFormat;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.FragmentTransaction;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.tns_energo_pnz.app.FileUtils;
import com.tns_energo_pnz.app.R;
import com.tns_energo_pnz.app.RecyclerViewAdapters.MediaAdapter;
import com.tns_energo_pnz.app.activities.BaseActivity;

import java.util.ArrayList;
import java.util.List;


public class FillingCheckBoxesFragment extends BaseFragment {
    private ActivityResultLauncher<Intent> imagePickerLauncher;
    private MediaAdapter mediaAdapter;
    private final int REQUEST_CODE_READ_EXTERNAL_STORAGE = 41;

    public static FillingCheckBoxesFragment newInstance(int type_work, String address) {
        Bundle args = new Bundle();
        args.putInt("TYPE_WORK", type_work);
        args.putString("ADDRESS", address);
        return BaseFragment.newInstance(FillingCheckBoxesFragment.class, args);
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_filling_checkboxes, container, false);
        initImageAdapter(view);
        setEventListeners(view);
        registerActivityResultLauncher();
        setFragment();
        return view;
    }

    private void setEventListeners(View view){
        Button confirm = view.findViewById(R.id.confirm);
        Button back = view.findViewById(R.id.back_button);
        ImageButton pick_image = view.findViewById(R.id.image_pick);
        confirm.setOnClickListener(this::confirm);
        back.setOnClickListener(v -> ((BaseActivity)getActivity()).switchFragment(new StartFillingFragment()));
        pick_image.setOnClickListener(v -> {
            getPermission(v);
            Intent intent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
            intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
            imagePickerLauncher.launch(intent);
        });
    }

    private void confirm(View view){
        String filename = "photo";
        String address = getArguments().getString("ADDRESS").replace(".", "_");
        String formattedDateTime = DateFormat.format("dd_MM_yyyy_HH_mm", new java.util.Date()).toString();
        String dirname = String.format("%s_%s", address, formattedDateTime);
        String fullPathToDir = String.format(view.getContext().getFilesDir() + "/%s", dirname);
        List<Uri> uris = mediaAdapter.getImageUris();
        for (int i = 0; i < uris.size(); i++) {
            FileUtils.copyFileFromUri(view.getContext(), uris.get(i), String.format("%s/%s%d%s", fullPathToDir, filename, i, ".jpg"));
        }
        ((BaseActivity)getActivity()).switchFragment(new OverviewFragment());
    }

    private void initImageAdapter(View view) {
        RecyclerView recyclerView = view.findViewById(R.id.message_images);
        recyclerView.setLayoutManager(new GridLayoutManager(view.getContext(), 3));
        recyclerView.setVisibility(View.GONE);
        mediaAdapter = new MediaAdapter(view.getContext(), new ArrayList<>());
        recyclerView.setAdapter(mediaAdapter);
    }

    private void getPermission(View view) {
        if (ContextCompat.checkSelfPermission(view.getContext(), Manifest.permission.READ_EXTERNAL_STORAGE)
                != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(requireActivity(),
                    new String[]{Manifest.permission.READ_EXTERNAL_STORAGE},
                    REQUEST_CODE_READ_EXTERNAL_STORAGE);
        }
    }

    private void registerActivityResultLauncher(){
        imagePickerLauncher = registerForActivityResult(
                new ActivityResultContracts.StartActivityForResult(),
                result -> {
                    if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                        Intent data = result.getData();
                        handleMediaPickerResult(data);
                    }
                }
        );
    }

    private void handleMediaPickerResult(Intent data) {
        List<Uri> mediaList = new ArrayList<>();
        if (data.getClipData() != null) {
            int count = data.getClipData().getItemCount();
            for (int i = 0; i < count; i++) {
                Uri mediaUri = data.getClipData().getItemAt(i).getUri();
                mediaList.add(mediaUri);
            }
        } else if (data.getData() != null) {
            Uri imageUri = data.getData();
            mediaList.add(imageUri);
        }
        mediaAdapter.setImageUris(mediaList);
    }

    private void setFragment() {
        FragmentTransaction fragmentTransaction = getChildFragmentManager().beginTransaction();
        switch (getArguments().getInt("TYPE_WORK")){
            case 0:
                fragmentTransaction.add(R.id.fragment_container, new LimitControllerFragment());
                break;
            case 1:
                fragmentTransaction.add(R.id.fragment_container, new StopLimitFragment());
                break;
            case 2:
                fragmentTransaction.add(R.id.fragment_container, new ReturningFragment());
                break;
        }
        fragmentTransaction.commit();
    }
}
