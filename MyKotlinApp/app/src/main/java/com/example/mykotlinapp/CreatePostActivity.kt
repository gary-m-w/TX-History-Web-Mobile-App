package com.example.mykotlinapp

import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.os.Bundle
import android.provider.MediaStore
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import kotlinx.android.synthetic.main.create_post.*
import kotlinx.android.synthetic.main.video_row.*
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import java.io.ByteArrayOutputStream
import java.io.IOException

private const val REQUEST_CODE = 1

class CreatePostActivity: AppCompatActivity() {

    val config: Bitmap.Config = Bitmap.Config.ARGB_8888
    var imagestored : Bitmap = Bitmap.createBitmap(500, 500, config)
    companion object {
        private const val CAMERA_PERMISSION_CODE = 1
        private const val CAMERA = 2
    }
    val REQUEST_IMAGE_CAPTURE = 1

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.create_post)

        val btncamera = findViewById<Button>(R.id.btn_camera)

        btncamera.setOnClickListener {
            if (ContextCompat.checkSelfPermission(
                    this,
                    android.Manifest.permission.CAMERA
                ) == PackageManager.PERMISSION_GRANTED
            ) {
                val intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
                //startActivityForResult(intent, REQUEST_CODE)
                startActivity(intent)
            } else {
                ActivityCompat.requestPermissions(
                    this,
                    arrayOf(android.Manifest.permission.CAMERA),
                    CAMERA_PERMISSION_CODE
                )
            }
        }

        val btn_submit_form= findViewById<Button>(R.id.submit_button)
        btn_submit_form.setOnClickListener{
            postData()
            val intent = Intent(this, ThemeActivity::class.java)
            startActivity(intent)
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == Activity.RESULT_OK) {
            println("inside on activity result")
            imagestored = data?.extras?.get("data") as Bitmap
            //imageView3.setImageBitmap(imagestored)
            imageView_video_thumbnail.setImageBitmap(imagestored)
        } else {
            super.onActivityResult(requestCode,resultCode,data);
        }
    }

    fun postData(){

        val url = "http://homework5apad.uw.r.appspot.com/post"

        val title= findViewById<EditText>(R.id.Title_input).text.toString()
        println("line 31"+title)
        val description= findViewById<EditText>(R.id.Description_input).text.toString()
        println("line 33"+description)
//        val tag= findViewById<EditText>(R.id.description_input).text.toString()
//        println(tag)
//        val theme= findViewById<EditText>(R.id.spinner2).text.toString()
//        println(theme)
        val client = OkHttpClient()
        println("line 35")

        val stream = ByteArrayOutputStream()
        imagestored.compress(Bitmap.CompressFormat.JPEG, 60, stream)
        println("line 86 byte array test")
        val byteArray: ByteArray = stream.toByteArray()
        println(byteArray.toString())


        val requestBody = MultipartBody.Builder()
            .setType(MultipartBody.FORM)
            .addFormDataPart("title", title)
            .addFormDataPart("description", description)
            .addFormDataPart("image", "filename.jpg",
                RequestBody.create("image/*jpg".toMediaTypeOrNull(), byteArray))
            .addFormDataPart("theme", "building")
            .addFormDataPart("tag", "wow")
            .addFormDataPart("location", "texas")
            .addFormDataPart("locality", "austin")
            .addFormDataPart("administrative_area_level_1", "texas")
            .build()


        val request = Request.Builder()
            .url(url)
            .post(requestBody)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onResponse(call: okhttp3.Call, response: Response) {
                val body = response.body?.string()
                println(body)

            }

            override fun onFailure(call: okhttp3.Call, e: IOException) {
                println("Failed to post")
                println(e)
            }
        })
    }



}