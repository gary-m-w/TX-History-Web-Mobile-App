package com.example.mykotlinapp

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.google.gson.GsonBuilder
import kotlinx.android.synthetic.main.placeholer.*
import okhttp3.*
import java.io.IOException
import android.content.Intent
import android.widget.Button


class MemorialActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.placeholer)

        val button_themes = findViewById<Button>(R.id.button_theme)

        //recyclerView_main.setBackgroundColor(Color.BLUE)
        recyclerView_main.layoutManager = LinearLayoutManager( this )
        //recyclerView_main.adapter = MainAdapter()

        fetchJson()

        button_themes.setOnClickListener{
            val intent = Intent(this, ThemeActivity::class.java)
            startActivity(intent)
        }
    }

    fun fetchJson(){
        println("Attempting to fetch")

        val url = "https://homework5apad.uw.r.appspot.com/api/theme_search_name/Memorial"

        val request = Request.Builder().url(url).build()
        val client = OkHttpClient()
        client.newCall(request).enqueue(object: Callback {

            override fun onResponse(call: Call, response: Response) {
                val body = response.body?.string()
                println(body)

                val gson = GsonBuilder().create()
                val homeFeed =  gson.fromJson(body,Array<HomeFeed>::class.java)

                runOnUiThread{
                    recyclerView_main.adapter =  MainAdapter(homeFeed)
                }
            }
            override fun onFailure(call: Call, e: IOException) {
                println("Failed to execute request")
            }
        })
    }
}

