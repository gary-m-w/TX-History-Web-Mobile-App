package com.example.mykotlinapp

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.google.gson.GsonBuilder
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.activity_theme.*
import okhttp3.*
import java.io.IOException

class ThemeActivity: AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_theme)

        val button_park = findViewById<Button>(R.id.button_park)
        val button_building = findViewById<Button>(R.id.button_building)
        val button_museum = findViewById<Button>(R.id.button_museum)
        val button_statue = findViewById<Button>(R.id.button_statue)
        val button_memorial = findViewById<Button>(R.id.button_memorial)
        val button_all = findViewById<Button>(R.id.button_all)

        recyclerView_theme.layoutManager = LinearLayoutManager (this)
        //recyclerView_main.adapter = CourseDetailAdapter()
        fetchJson()

        button_park.setOnClickListener{
            val intent = Intent(this, ParkActivity::class.java)
            startActivity(intent)
        }
        button_statue.setOnClickListener{
            val intent = Intent(this, StatueActivity::class.java)
            startActivity(intent)
        }
        button_building.setOnClickListener{
            val intent = Intent(this, BuildingActivity::class.java)
            startActivity(intent)
        }
        button_museum.setOnClickListener{
            val intent = Intent(this, MusuemActivity::class.java)
            startActivity(intent)
        }
        button_memorial.setOnClickListener{
            val intent = Intent(this, MemorialActivity::class.java)
            startActivity(intent)
        }
        button_all.setOnClickListener{
            val intent = Intent(this, PostActivity::class.java)
            startActivity(intent)
        }
        button_createpost.setOnClickListener{
            val intent = Intent(this, CreatePostActivity::class.java)
            startActivity(intent)
        }
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
                    recyclerView_theme.adapter =  ThemeAdapter(themeFeed)
                }
            }
            override fun onFailure(call: Call, e: IOException) {
                println("Failed to execute request")
            }
        })
    }


}