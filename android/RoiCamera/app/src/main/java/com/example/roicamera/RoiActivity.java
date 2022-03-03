package com.example.roicamera;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.widget.ImageView;


public class RoiActivity extends AppCompatActivity {
    ImageView roi_img;
    Bitmap image;
    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_roi);
        roi_img=(ImageView)findViewById(R.id.roi_photo);

        Intent intent = getIntent();
        byte[] arr = intent.getByteArrayExtra("roi");
        image= BitmapFactory.decodeByteArray(arr, 0, arr.length);
        roi_img.setImageBitmap(image);
    }
}
