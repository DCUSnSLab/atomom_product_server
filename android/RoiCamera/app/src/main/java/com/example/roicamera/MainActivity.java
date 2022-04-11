package com.example.roicamera;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.annotation.TargetApi;
import android.content.pm.PackageManager;
import android.os.Build;
import android.provider.MediaStore;
import android.util.Log;
import android.view.SurfaceView;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.LoaderCallbackInterface;
import org.opencv.android.OpenCVLoader;
import org.opencv.android.Utils;
import org.opencv.core.Mat;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.imgproc.Imgproc;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLDecoder;
import java.util.Collections;
import java.util.List;

import static android.Manifest.permission.CAMERA;


public class MainActivity extends AppCompatActivity
        implements CameraBridgeViewBase.CvCameraViewListener2{

    private static final String TAG = "camera";
    private Mat matInput;
    private Mat m_matRoi;
    Bitmap bmp_result;
    Button roi_capture;
    Rect rect;
    Rect roi_rect;
    private CameraBridgeViewBase mOpenCvCameraView;

    static {
        System.loadLibrary("opencv_java4");
        System.loadLibrary("native-lib");
    }


    private BaseLoaderCallback mLoaderCallback = new BaseLoaderCallback(this) {
        @Override
        public void onManagerConnected(int status) {
            switch (status) {
                case LoaderCallbackInterface.SUCCESS:
                {
                    mOpenCvCameraView.enableView();
                } break;
                default:
                {
                    super.onManagerConnected(status);
                } break;
            }
        }
    };


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        roi_capture = (Button)findViewById(R.id.btn_capture);

        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON,
                WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        setContentView(R.layout.activity_main);

        mOpenCvCameraView = (CameraBridgeViewBase)findViewById(R.id.activity_surface_view);
        mOpenCvCameraView.setVisibility(SurfaceView.VISIBLE);
        mOpenCvCameraView.setCvCameraViewListener(this);
        mOpenCvCameraView.setCameraIndex(0); // front-camera(1),  back-camera(0)
    }

    @Override
    public void onPause()
    {
        super.onPause();
        if (mOpenCvCameraView != null)
            mOpenCvCameraView.disableView();
    }

    @Override
    public void onResume()
    {
        super.onResume();

        if (!OpenCVLoader.initDebug()) {
            Log.d(TAG, "onResume :: Internal OpenCV library not found.");
            OpenCVLoader.initAsync(OpenCVLoader.OPENCV_VERSION_3_2_0, this, mLoaderCallback);
        } else {
            Log.d(TAG, "onResum :: OpenCV library found inside package. Using it!");
            mLoaderCallback.onManagerConnected(LoaderCallbackInterface.SUCCESS);
        }
    }


    public void onDestroy() {
        super.onDestroy();

        if (mOpenCvCameraView != null)
            mOpenCvCameraView.disableView();
    }

    @Override
    public void onCameraViewStarted(int width, int height) {

    }

    @Override
    public void onCameraViewStopped() {

    }

    @Override
    public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {

        matInput = inputFrame.rgba();

        // ROI size
        double m_dWscale = (double)  1/4;
        double m_dHscale = (double) 1/2;

        int mRoiWidth = (int)(matInput.size().width * m_dWscale);
        int mRoiHeight = (int)(matInput.size().height * m_dHscale);

        int mRoiX = (int) (matInput.size().width - mRoiWidth) / 2;
        int mRoiY = (int) (matInput.size().height - mRoiHeight) / 2;

        rect = new Rect(mRoiX,mRoiY,mRoiWidth,mRoiHeight);
        Imgproc.rectangle(matInput,rect,new Scalar(0, 255, 0, 255),5);

        roi_rect = new Rect(mRoiX+4,mRoiY+4,mRoiWidth-8,mRoiHeight-8);
        m_matRoi = matInput.submat(roi_rect);

        return matInput;
    }


    protected List<? extends CameraBridgeViewBase> getCameraViewList() {
        return Collections.singletonList(mOpenCvCameraView);
    }


    //여기서부턴 퍼미션 관련 메소드
    private static final int CAMERA_PERMISSION_REQUEST_CODE = 200;


    protected void onCameraPermissionGranted() {
        List<? extends CameraBridgeViewBase> cameraViews = getCameraViewList();
        if (cameraViews == null) {
            return;
        }
        for (CameraBridgeViewBase cameraBridgeViewBase: cameraViews) {
            if (cameraBridgeViewBase != null) {
                cameraBridgeViewBase.setCameraPermissionGranted();
            }
        }
    }

    @Override
    protected void onStart() {
        super.onStart();
        boolean havePermission = true;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (checkSelfPermission(CAMERA) != PackageManager.PERMISSION_GRANTED) {
                requestPermissions(new String[]{CAMERA}, CAMERA_PERMISSION_REQUEST_CODE);
                havePermission = false;
            }
        }
        if (havePermission) {
            onCameraPermissionGranted();
        }
    }

    @Override
    @TargetApi(Build.VERSION_CODES.M)
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        if (requestCode == CAMERA_PERMISSION_REQUEST_CODE && grantResults.length > 0
                && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            onCameraPermissionGranted();
        }else{
            showDialogForPermission("앱을 실행하려면 퍼미션을 허가하셔야합니다.");
        }
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }


    @TargetApi(Build.VERSION_CODES.M)
    private void showDialogForPermission(String msg) {

        AlertDialog.Builder builder = new AlertDialog.Builder( MainActivity.this);
        builder.setTitle("알림");
        builder.setMessage(msg);
        builder.setCancelable(false);
        builder.setPositiveButton("예", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int id){
                requestPermissions(new String[]{CAMERA}, CAMERA_PERMISSION_REQUEST_CODE);
            }
        });
        builder.setNegativeButton("아니오", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface arg0, int arg1) {
                finish();
            }
        });
        builder.create().show();
    }


    public void onClick(View view) {
        switch(view.getId()) {
            case R.id.btn_capture: {
                bmp_result = Bitmap.createBitmap(m_matRoi.cols(),m_matRoi.rows(),Bitmap.Config.ARGB_8888);
                Utils.matToBitmap(m_matRoi,bmp_result);

                Intent intent_img = new Intent(getApplicationContext(),RoiActivity.class);
                ByteArrayOutputStream stream = new ByteArrayOutputStream();

                bmp_result.compress(Bitmap.CompressFormat.JPEG, 100, stream);

                new Thread(() -> {
                    UploadFile(bmp_result);
                }).start();

//                MediaStore.Images.Media.insertImage(getContentResolver(), bmp_result, "Test" , "testimage");

//                UploadFile(bmp_result);

//                byte[] byteArray = stream.toByteArray();
//                intent_img.putExtra("roi",byteArray);
//                intent_img.putExtra("text", "test text test\n");
//                startActivity(intent_img);
//                startActivity(intent_text);
            }
        }
    }

    public void UploadFile(final Bitmap bitmap){
        HttpURLConnection con = null;
        StringBuffer sbParams = new StringBuffer();
        String text2="";
        Intent intent_text = new Intent(getApplicationContext(),RoiActivity.class);
        intent_text.putExtra("text", "test test test\n");

        try {
            URL url = new URL("http://203.250.32.251:8000/api?rows=960&cols=960");
            String lineEnd = "\r\n";
            String twoHyphens = "--";
            String boundary = "*****";
            // open connection
//            HttpURLConnection con = (HttpURLConnection)url.openConnection();
            con = (HttpURLConnection)url.openConnection();
            con.setDoInput(true); //input 허용
            con.setDoOutput(true);  // output 허용
            con.setUseCaches(false);   // cache copy를 허용하지 않는다.
            con.setRequestMethod("POST");
            con.setRequestProperty("Connection", "Keep-Alive");
            con.setRequestProperty("Content-Type", "multipart/form-data;boundary=" + boundary);

//            con.setRequestProperty("Accept-Charset", "UTF-8"); // Accept-Charset 설정.
//            con.setRequestProperty("Context_Type", "application/x-www-form-urlencoded;cahrset=UTF-8");
//
//            String strParams = "제발 연결.... 제발....";
            // write data
            DataOutputStream dos = new DataOutputStream(con.getOutputStream());
            ByteArrayOutputStream blob = new ByteArrayOutputStream();
            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, blob);
            byte[] bytes = blob.toByteArray();

            dos.writeBytes(twoHyphens + boundary + lineEnd);

            // 파일 전송시 파라메터명은 file1 파일명은 camera.jpg로 설정하여 전송
            dos.writeBytes("Content-Disposition: form-data; name=\"media\";filename=\"camera.jpg\"" + lineEnd);


            dos.writeBytes(lineEnd);
            dos.write(bytes);
            dos.writeBytes(lineEnd);
            dos.writeBytes(twoHyphens + boundary + twoHyphens + lineEnd);
            dos.flush(); // finish upload...
            dos.close();

//            dos.write(strParams.getBytes("UTF-8")); // 출력 스트림에 출력.
//            dos.flush(); // 출력 스트림을 플러시(비운다)하고 버퍼링 된 모든 출력 바이트를 강제 실행.
//            dos.close(); // 출력 스트림을 닫고 모든 시스템 자원을 해제.

            if (con.getResponseCode() != HttpURLConnection.HTTP_OK){
                text2+="유감쓰\n";
                intent_text.putExtra("text", text2);
            }

            BufferedReader reader = new BufferedReader(new InputStreamReader(con.getInputStream(), "UTF-8"));

            // 출력물의 라인과 그 합에 대한 변수.
            String line;
            String page = "";

            // 라인을 받아와 합친다.
//            while ((line = reader.readLine()) != null){
//                page += line;
//            }
            while(true){
                line = reader.readLine();
                if(line == null){
                    break;
                }
                page = line+"\n";
            }

//            String test = URLDecoder.decode(page, "utf-8");

//            text2+=test;
//            intent_text.putExtra("text", test);
            text2+=page;
            intent_text.putExtra("text", page);

        } catch (MalformedURLException e) { // for URL.
            text2+=e;
            intent_text.putExtra("text", text2);
        } catch (IOException e) { // for openConnection().
            text2+=e;
            intent_text.putExtra("text", text2);
        } catch (Exception e) {
            text2+=e;
            intent_text.putExtra("text", text2);
        } finally {
            if (con != null)
                con.disconnect();
        }

        startActivity(intent_text);
    }

}