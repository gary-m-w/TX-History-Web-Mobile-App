package com.example.mykotlinapp

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.google.gson.GsonBuilder
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.activity_theme.*
import okhttp3.*
import java.io.IOException

class CourseDetailActivity: AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_theme)

        recyclerView_theme.layoutManager = LinearLayoutManager (this)
        //recyclerView_main.adapter = CourseDetailAdapter()
        fetchJson()
    }

    fun fetchJson(){
        println("Attempting to fetch")

        val url = "https://homework5apad.uw.r.appspot.com/api/themes"

        val request = Request.Builder().url(url).build()
        val client = OkHttpClient()
        client.newCall(request).enqueue(object: Callback {

            override fun onResponse(call: Call, response: Response) {
                val body = response.body?.string()
                println(body)

                val gson = GsonBuilder().create()
                val themeFeed =  gson.fromJson(body,Array<ThemeFeed>::class.java)

                runOnUiThread{
                    recyclerView_theme.adapter =  CourseDetailAdapter(themeFeed)
                }
            }
            override fun onFailure(call: Call, e: IOException) {
                println("Failed to execute request")
            }
        })
    }


}